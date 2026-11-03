"""Baixa dados intradiários dos perpétuos USDT-M da Binance (data.binance.vision).

- Candles de 1 minuto (com volume agressor comprador) → <DATA>/intraday/<SYM>_1m.parquet
- Métricas de 5 minutos (open interest, razão long/short de contas e top traders,
  razão de volume agressor) → <DATA>/intraday/<SYM>_metrics.parquet

Uso: python research/data/download_intraday.py [DATA_DIR] [SYM ...]
"""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from download_binance import FILES, _get, _read_zip_csv, s3_list  # noqa: E402

KL = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume",
      "trades", "taker_buy_base", "taker_buy_quote", "ignore"]
MET = ["create_time", "symbol", "oi", "oi_value", "top_acc_ls", "top_pos_ls", "acc_ls", "taker_ls_vol"]


def _kl(key: str) -> pd.DataFrame | None:
    try:
        df = _read_zip_csv(_get(FILES + key), KL)
    except Exception as e:  # noqa: BLE001
        print("erro", key, e, file=sys.stderr)
        return None
    df = df.drop(columns=["close_time", "ignore"])
    df["open_time"] = pd.to_numeric(df["open_time"])
    df.loc[df.open_time > 10**14, "open_time"] //= 1000
    for c in df.columns[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("float64" if c in ("open", "high", "low", "close") else "float32")
    return df


def _met(key: str) -> pd.DataFrame | None:
    try:
        df = _read_zip_csv(_get(FILES + key), MET)
    except Exception as e:  # noqa: BLE001
        print("erro", key, e, file=sys.stderr)
        return None
    df["ts"] = pd.to_datetime(df["create_time"])
    df = df.drop(columns=["create_time", "symbol"])
    for c in MET[2:]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("float32")
    return df


def klines(sym: str, out: Path) -> None:
    dest = out / f"{sym}_1m.parquet"
    if dest.exists():
        return
    keys = sorted(k for k in s3_list(f"data/futures/um/monthly/klines/{sym}/1m/", dirs=False) if k.endswith(".zip"))
    with ThreadPoolExecutor(8) as ex:
        frames = [f for f in ex.map(_kl, keys) if f is not None]
    df = pd.concat(frames).drop_duplicates("open_time").sort_values("open_time")
    df.to_parquet(dest, index=False)
    print(sym, "1m:", len(df), "linhas", flush=True)


def metrics(sym: str, out: Path) -> None:
    dest = out / f"{sym}_metrics.parquet"
    if dest.exists():
        return
    keys = sorted(k for k in s3_list(f"data/futures/um/daily/metrics/{sym}/", dirs=False) if k.endswith(".zip"))
    with ThreadPoolExecutor(24) as ex:
        frames = [f for f in ex.map(_met, keys) if f is not None]
    df = pd.concat(frames).drop_duplicates("ts").sort_values("ts")
    df.to_parquet(dest, index=False)
    print(sym, "metrics:", len(df), "linhas", flush=True)


def main() -> None:
    base = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/rawdata") / "intraday"
    base.mkdir(parents=True, exist_ok=True)
    syms = sys.argv[2:] or ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT", "XRPUSDT"]
    for s in syms:
        klines(s, base)
        metrics(s, base)


if __name__ == "__main__":
    main()
