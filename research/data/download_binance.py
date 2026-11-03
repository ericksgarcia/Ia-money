"""Baixa dados públicos da Binance (data.binance.vision, documentado em
github.com/binance/binance-public-data) para pesquisa.

- Spot: candles diários (1d) de TODOS os pares USDT, inclusive deslistados
  (evita viés de sobrevivência).
- Futuros USDT-M: histórico de funding rate de todos os perpétuos.

Uso: python research/data/download_binance.py [DATA_DIR]
"""
from __future__ import annotations

import io
import re
import sys
import zipfile
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

S3 = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
FILES = "https://data.binance.vision/"
NS = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}

STABLE = {"USDC", "BUSD", "TUSD", "USDP", "PAX", "DAI", "FDUSD", "UST", "USDS",
          "USDSB", "SUSD", "EUR", "GBP", "AUD", "BRL", "TRY", "RUB", "UAH",
          "NGN", "BIDR", "IDRT", "BVND", "AEUR", "EURI", "USD1", "XUSD", "RLUSD",
          "BKRW", "ZAR", "JPY", "COP", "ARS", "MXN", "PLN", "RON", "CZK", "USDE",
          "PYUSD", "U", "BFUSD", "USDF"}
LEVERAGED = re.compile(r"(UP|DOWN|BULL|BEAR)USDT$")


def _get(url: str, timeout: int = 60) -> bytes:
    url = urllib.parse.quote(url, safe=":/?&=%")  # símbolos com caracteres não-ASCII
    req = urllib.request.Request(url, headers={"User-Agent": "research-downloader"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception:
            if attempt == 3:
                raise
    raise RuntimeError(url)


def s3_list(prefix: str, dirs: bool) -> list[str]:
    out, marker = [], ""
    while True:
        url = f"{S3}?delimiter=/&prefix={prefix}" + (f"&marker={marker}" if marker else "")
        root = ET.fromstring(_get(url))
        if dirs:
            items = [p.find("s3:Prefix", NS).text for p in root.findall("s3:CommonPrefixes", NS)]
        else:
            items = [c.find("s3:Key", NS).text for c in root.findall("s3:Contents", NS)]
        out += items
        if root.find("s3:IsTruncated", NS).text != "true":
            return out
        nxt = root.find("s3:NextMarker", NS)
        marker = nxt.text if nxt is not None else items[-1]


def _read_zip_csv(blob: bytes, names: list[str]) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        raw = z.read(z.namelist()[0]).decode()
    first = raw.split("\n", 1)[0]
    header = 0 if re.search(r"[a-zA-Z]", first) else None
    df = pd.read_csv(io.StringIO(raw), header=header)
    df = df.iloc[:, : len(names)]
    df.columns = names
    return df


def _to_dt(ts: pd.Series) -> pd.Series:
    ts = pd.to_numeric(ts)
    # Binance passou a usar microssegundos nos arquivos spot a partir de 2025
    ts = ts.where(ts < 10**14, ts // 1000)
    return pd.to_datetime(ts, unit="ms", utc=True)


def spot_symbol(sym: str, out_dir: Path) -> str:
    try:
        return _spot_symbol(sym, out_dir)
    except Exception as e:
        print("falhou", sym, e, file=sys.stderr)
        return "error"


def _spot_symbol(sym: str, out_dir: Path) -> str:
    dest = out_dir / f"{sym}.csv"
    if dest.exists():
        return "skip"
    keys = [k for k in s3_list(f"data/spot/monthly/klines/{sym}/1d/", dirs=False) if k.endswith(".zip")]
    frames = []
    for k in keys:
        try:
            frames.append(_read_zip_csv(_get(FILES + k), [
                "open_time", "open", "high", "low", "close", "volume", "close_time",
                "quote_volume", "trades", "taker_base", "taker_quote", "ignore"]))
        except Exception as e:  # arquivo corrompido/ausente: segue
            print("erro", k, e, file=sys.stderr)
    if not frames:
        return "empty"
    df = pd.concat(frames)
    df["date"] = _to_dt(df["open_time"]).dt.date
    df = df[["date", "open", "high", "low", "close", "volume", "quote_volume"]]
    df.drop_duplicates("date").sort_values("date").to_csv(dest, index=False)
    return "ok"


def funding_symbol(sym: str, out_dir: Path) -> str:
    try:
        return _funding_symbol(sym, out_dir)
    except Exception as e:
        print("falhou", sym, e, file=sys.stderr)
        return "error"


def _funding_symbol(sym: str, out_dir: Path) -> str:
    dest = out_dir / f"{sym}.csv"
    if dest.exists():
        return "skip"
    keys = [k for k in s3_list(f"data/futures/um/monthly/fundingRate/{sym}/", dirs=False) if k.endswith(".zip")]
    frames = []
    for k in keys:
        try:
            frames.append(_read_zip_csv(_get(FILES + k), ["calc_time", "interval_h", "rate"]))
        except Exception as e:
            print("erro", k, e, file=sys.stderr)
    if not frames:
        return "empty"
    df = pd.concat(frames)
    df["time"] = _to_dt(df["calc_time"])
    df[["time", "rate"]].drop_duplicates("time").sort_values("time").to_csv(dest, index=False)
    return "ok"


def main() -> None:
    base = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/rawdata/binance")
    (base / "spot_1d").mkdir(parents=True, exist_ok=True)
    (base / "funding").mkdir(parents=True, exist_ok=True)

    spot = [p.rstrip("/").split("/")[-1] for p in s3_list("data/spot/monthly/klines/", dirs=True)]
    spot = [s for s in spot if s.endswith("USDT") and s[:-4] not in STABLE and not LEVERAGED.search(s)]
    print(f"spot USDT symbols: {len(spot)}", flush=True)
    with ThreadPoolExecutor(32) as ex:
        res = list(ex.map(lambda s: spot_symbol(s, base / "spot_1d"), spot))
    print("spot:", pd.Series(res).value_counts().to_dict(), flush=True)

    (base / "perp_1d").mkdir(parents=True, exist_ok=True)
    for sym in ["BTCUSDT", "ETHUSDT"]:  # candles do perpétuo (para medir a base spot×perp no carry)
        keys = [k for k in s3_list(f"data/futures/um/monthly/klines/{sym}/1d/", dirs=False) if k.endswith(".zip")]
        df = pd.concat(_read_zip_csv(_get(FILES + k), [
            "open_time", "open", "high", "low", "close", "volume", "close_time",
            "quote_volume", "trades", "taker_base", "taker_quote", "ignore"]) for k in keys)
        df["date"] = _to_dt(df["open_time"]).dt.date
        df[["date", "close"]].drop_duplicates("date").sort_values("date").to_csv(base / "perp_1d" / f"{sym}.csv", index=False)

    fut = [p.rstrip("/").split("/")[-1] for p in s3_list("data/futures/um/monthly/fundingRate/", dirs=True)]
    fut = [s for s in fut if s.endswith("USDT")]
    print(f"funding symbols: {len(fut)}", flush=True)
    with ThreadPoolExecutor(32) as ex:
        res = list(ex.map(lambda s: funding_symbol(s, base / "funding"), fut))
    print("funding:", pd.Series(res).value_counts().to_dict(), flush=True)


if __name__ == "__main__":
    main()
