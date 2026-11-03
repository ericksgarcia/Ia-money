"""Economia real de um revendedor brasileiro de keys (G2A, Gamivo, Kinguin), 2021–2023.

Lê planilhas públicas de um revendedor (encontradas no GitHub) e imprime SÓ estatísticas agregadas.
As planilhas contêm dados pessoais de clientes (e-mails, perfis, keys): este script descarta essas
colunas antes de qualquer cálculo e nunca as imprime. Por privacidade, o endereço do repositório de
origem não é reproduzido aqui.

Uso: python -I research/keys/agregados_revenda.py <planilha_operacoes.xlsx> <planilha_taxas.xlsx>
"""
import sys

import pandas as pd

f_ops, f_fee = sys.argv[1], sys.argv[2]
df = pd.read_excel(f_ops, sheet_name="Venda-Chave-Troca")
keep = [c for c in df.columns if c in ("Jogo HB", "Vendido por", "Valor G2A", "Colunas2", "V.R. (Real)", "V. R. (Simulação)", "Jogo Entregue", "Valor Pago", "Vendido", "Leilões/Mudanças de Preço", "Qtd", "Devoluções")]
df = df[keep]
for c in ["Valor G2A", "Colunas2", "V.R. (Real)", "Valor Pago", "Vendido", "Leilões/Mudanças de Preço", "Qtd", "Devoluções"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
v = df[df["Valor Pago"].notna() & df["Valor G2A"].notna()]
print("operações com custo e preço:", len(v), "| vendidas:", int((v["Vendido"] == 1).sum()))
print("canais:", v["Vendido por"].value_counts().head(5).to_dict())
s = v[v["Vendido"] == 1] if (v["Vendido"] == 1).sum() > 20 else v
print("base de cálculo:", "vendidas" if s is not v else "todas (vendidas < 20)", len(s))
print(s[["Valor G2A", "V.R. (Real)", "Valor Pago", "Leilões/Mudanças de Preço"]].describe(percentiles=[.1, .5, .9]).round(3).T.to_string())
net = s["V.R. (Real)"]; cost = s["Valor Pago"]; px = s["Valor G2A"]
print("recebido/preço de vitrine: mediana", round((net / px).median(), 3))
lucro = net - cost
print(f"lucro por key (€): média {lucro.mean():.3f}, mediana {lucro.median():.3f}, p10 {lucro.quantile(.1):.3f}, p90 {lucro.quantile(.9):.3f}")
print(f"margem sobre custo: mediana {(lucro / cost).median()*100:.0f}%, % com prejuízo {(lucro < 0).mean()*100:.0f}%")
print(f"faixa de preço de venda: {(px < 1).mean()*100:.0f}% abaixo de €1, {(px.between(1, 5)).mean()*100:.0f}% entre €1–5, {(px > 5).mean()*100:.0f}% acima de €5")
print("origem (amostra de descrições de pagamento, sem dados pessoais):", s["Jogo Entregue"].astype(str).str.extract(r"(TF2|PayPal|Pix|USDT|BTC|Steam)", expand=False).value_counts().to_dict())
print("devoluções:", int(s["Devoluções"].fillna(0).gt(0).sum()), "de", len(s))
# tabela de taxas
for sh in ["#02", "#03"]:
    t = pd.read_excel(f_fee, sheet_name=sh)
    print(f"--- taxa G2A [{sh}]")
    cols = [c for c in t.columns if "Preço" in str(c) or "Diferença" in str(c)]
    print(t[cols].dropna(how="all").head(40).round(3).to_string())
