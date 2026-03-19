"""
Análise do Mercado de TI no Brasil — 2024
Autor: Leonardo Carrer Lemos
Ferramentas: Python, Pandas, Matplotlib, Seaborn
Dataset: Simulado com base na pesquisa Stack Overflow Developer Survey 2024
         e dados do mercado brasileiro de tecnologia
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import os

# ── Configurações visuais ──────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.facecolor": "#F8F9FA",
    "axes.facecolor":   "#F8F9FA",
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   14,
    "axes.titleweight": "bold",
    "axes.labelsize":   11,
})

os.makedirs("graficos", exist_ok=True)
os.makedirs("dados", exist_ok=True)

# ── 1. Criando o Dataset ───────────────────────────────────────────────────────
np.random.seed(42)
n = 500

cargos = [
    "Analista de Dados", "Cientista de Dados", "Engenheiro de Dados",
    "Desenvolvedor Backend", "Desenvolvedor Frontend", "Analista de TI",
    "DevOps / SRE", "Desenvolvedor Mobile", "QA / Tester"
]
cargos_pesos = [0.14, 0.10, 0.10, 0.18, 0.12, 0.12, 0.08, 0.09, 0.07]

estados = ["SP", "RJ", "MG", "RS", "PR", "SC", "DF", "BA", "PE"]
estados_pesos = [0.38, 0.16, 0.12, 0.09, 0.08, 0.07, 0.05, 0.03, 0.02]

modalidades = ["Remoto", "Híbrido", "Presencial"]
modalidades_pesos = [0.40, 0.38, 0.22]

senioridades = ["Júnior", "Pleno", "Sênior"]
senioridades_pesos = [0.30, 0.40, 0.30]

experiencia_anos = {
    "Júnior": (0, 2), "Pleno": (2, 5), "Sênior": (5, 15)
}

salarios_base = {
    ("Analista de Dados",     "Júnior"): 3500,
    ("Analista de Dados",     "Pleno"):  6500,
    ("Analista de Dados",     "Sênior"): 10000,
    ("Cientista de Dados",    "Júnior"): 5000,
    ("Cientista de Dados",    "Pleno"):  9000,
    ("Cientista de Dados",    "Sênior"): 15000,
    ("Engenheiro de Dados",   "Júnior"): 5500,
    ("Engenheiro de Dados",   "Pleno"):  10000,
    ("Engenheiro de Dados",   "Sênior"): 16000,
    ("Desenvolvedor Backend", "Júnior"): 4000,
    ("Desenvolvedor Backend", "Pleno"):  8000,
    ("Desenvolvedor Backend", "Sênior"): 13000,
    ("Desenvolvedor Frontend","Júnior"): 3500,
    ("Desenvolvedor Frontend","Pleno"):  7000,
    ("Desenvolvedor Frontend","Sênior"): 11000,
    ("Analista de TI",        "Júnior"): 2500,
    ("Analista de TI",        "Pleno"):  4500,
    ("Analista de TI",        "Sênior"): 7000,
    ("DevOps / SRE",          "Júnior"): 5000,
    ("DevOps / SRE",          "Pleno"):  9500,
    ("DevOps / SRE",          "Sênior"): 15000,
    ("Desenvolvedor Mobile",  "Júnior"): 4000,
    ("Desenvolvedor Mobile",  "Pleno"):  7500,
    ("Desenvolvedor Mobile",  "Sênior"): 12000,
    ("QA / Tester",           "Júnior"): 2800,
    ("QA / Tester",           "Pleno"):  5000,
    ("QA / Tester",           "Sênior"): 8000,
}

cargo_col       = np.random.choice(cargos, size=n, p=cargos_pesos)
senioridade_col = np.random.choice(senioridades, size=n, p=senioridades_pesos)
estado_col      = np.random.choice(estados, size=n, p=estados_pesos)
modalidade_col  = np.random.choice(modalidades, size=n, p=modalidades_pesos)

salario_col, exp_col = [], []
for cargo, sen in zip(cargo_col, senioridade_col):
    base   = salarios_base[(cargo, sen)]
    ruido  = np.random.normal(0, base * 0.12)
    salario_col.append(max(1500, round(base + ruido, -2)))
    lo, hi = experiencia_anos[sen]
    exp_col.append(round(np.random.uniform(lo, hi), 1))

tecnologias_por_cargo = {
    "Analista de Dados":     ["Python", "SQL", "Power BI", "Excel", "Tableau"],
    "Cientista de Dados":    ["Python", "SQL", "Machine Learning", "TensorFlow", "Spark"],
    "Engenheiro de Dados":   ["Python", "SQL", "Spark", "Airflow", "DBT"],
    "Desenvolvedor Backend": ["Python", "Java", "SQL", "Docker", "APIs REST"],
    "Desenvolvedor Frontend":["JavaScript", "React", "TypeScript", "CSS", "Node.js"],
    "Analista de TI":        ["Excel", "SQL", "Suporte", "Redes", "Linux"],
    "DevOps / SRE":          ["Docker", "Kubernetes", "Terraform", "Linux", "CI/CD"],
    "Desenvolvedor Mobile":  ["Kotlin", "Swift", "React Native", "Flutter", "APIs REST"],
    "QA / Tester":           ["Selenium", "Python", "Jest", "Postman", "SQL"],
}

todas_techs = set()
for v in tecnologias_por_cargo.values():
    todas_techs.update(v)
todas_techs = sorted(todas_techs)

tech_rows = []
for cargo in cargo_col:
    row = {t: 0 for t in todas_techs}
    for t in tecnologias_por_cargo[cargo]:
        row[t] = 1
    tech_rows.append(row)

df = pd.DataFrame({
    "cargo":       cargo_col,
    "senioridade": senioridade_col,
    "estado":      estado_col,
    "modalidade":  modalidade_col,
    "salario":     salario_col,
    "experiencia": exp_col,
})
df = pd.concat([df, pd.DataFrame(tech_rows)], axis=1)
df.to_csv("dados/mercado_ti_brasil.csv", index=False)
print(f"✅ Dataset criado: {len(df)} registros | {df.shape[1]} colunas\n")

# ── 2. Análise Exploratória ────────────────────────────────────────────────────
print("=" * 55)
print("  ANÁLISE DO MERCADO DE TI NO BRASIL — 2024")
print("=" * 55)

print("\n📊 Distribuição por cargo:")
print(df["cargo"].value_counts().to_string())

print("\n💰 Salário médio por cargo (R$):")
sal_cargo = df.groupby("cargo")["salario"].mean().sort_values(ascending=False)
for cargo, sal in sal_cargo.items():
    print(f"   {cargo:<28} R$ {sal:>8,.0f}")

print("\n🎯 Salário médio por senioridade (R$):")
order = ["Júnior", "Pleno", "Sênior"]
sal_sen = df.groupby("senioridade")["salario"].mean().reindex(order)
for sen, sal in sal_sen.items():
    print(f"   {sen:<10} R$ {sal:>8,.0f}")

print("\n🖥️  Distribuição por modalidade:")
print(df["modalidade"].value_counts().to_string())

# ── 3. Gráficos ────────────────────────────────────────────────────────────────
COR_DESTAQUE = "#2563EB"
COR_DADOS    = "#10B981"

# Gráfico 1 — Salário médio por cargo
fig, ax = plt.subplots(figsize=(11, 6))
sal_cargo_plot = df.groupby("cargo")["salario"].mean().sort_values()
cores = [COR_DESTAQUE if "Dados" in c or "Cientista" in c or "Engenheiro" in c
         else "#94A3B8" for c in sal_cargo_plot.index]
bars = ax.barh(sal_cargo_plot.index, sal_cargo_plot.values, color=cores, edgecolor="white", linewidth=0.8)
for bar in bars:
    ax.text(bar.get_width() + 150, bar.get_y() + bar.get_height() / 2,
            f"R$ {bar.get_width():,.0f}", va="center", fontsize=9, color="#374151")
ax.set_title("Salário Médio por Cargo em TI no Brasil (2024)", pad=15)
ax.set_xlabel("Salário Médio (R$)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
ax.set_xlim(0, sal_cargo_plot.max() * 1.22)
from matplotlib.patches import Patch
legend = [Patch(color=COR_DESTAQUE, label="Área de Dados"), Patch(color="#94A3B8", label="Outras áreas")]
ax.legend(handles=legend, loc="lower right")
plt.tight_layout()
plt.savefig("graficos/01_salario_por_cargo.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n✅ Gráfico 1 salvo: graficos/01_salario_por_cargo.png")

# Gráfico 2 — Boxplot salário por senioridade
fig, ax = plt.subplots(figsize=(9, 5))
palette = {"Júnior": "#93C5FD", "Pleno": "#3B82F6", "Sênior": "#1D4ED8"}
sns.boxplot(data=df, x="senioridade", y="salario", order=order,
            palette=palette, width=0.5, linewidth=1.2, ax=ax)
ax.set_title("Distribuição Salarial por Senioridade", pad=15)
ax.set_xlabel("Senioridade")
ax.set_ylabel("Salário (R$)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
plt.tight_layout()
plt.savefig("graficos/02_salario_senioridade.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Gráfico 2 salvo: graficos/02_salario_senioridade.png")

# Gráfico 3 — Tecnologias mais demandadas
tech_cols = [c for c in df.columns if c in todas_techs]
tech_counts = df[tech_cols].sum().sort_values(ascending=False).head(12)
fig, ax = plt.subplots(figsize=(10, 5))
cores_tech = [COR_DADOS if t in ["Python", "SQL", "Power BI", "Tableau", "Excel"]
              else COR_DESTAQUE for t in tech_counts.index]
ax.bar(tech_counts.index, tech_counts.values, color=cores_tech, edgecolor="white", linewidth=0.8)
ax.set_title("Top 12 Tecnologias Mais Demandadas no Mercado de TI", pad=15)
ax.set_ylabel("Nº de Vagas")
ax.set_xlabel("Tecnologia")
plt.xticks(rotation=35, ha="right")
legend2 = [Patch(color=COR_DADOS, label="Seu stack atual"), Patch(color=COR_DESTAQUE, label="Outras tecnologias")]
ax.legend(handles=legend2)
plt.tight_layout()
plt.savefig("graficos/03_tecnologias_demandadas.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Gráfico 3 salvo: graficos/03_tecnologias_demandadas.png")

# Gráfico 4 — Modalidade de trabalho
fig, ax = plt.subplots(figsize=(6, 6))
mod_counts = df["modalidade"].value_counts()
cores_mod = ["#2563EB", "#10B981", "#F59E0B"]
wedges, texts, autotexts = ax.pie(
    mod_counts, labels=mod_counts.index, autopct="%1.1f%%",
    colors=cores_mod, startangle=90,
    wedgeprops=dict(edgecolor="white", linewidth=2)
)
for at in autotexts:
    at.set_fontsize(11)
    at.set_fontweight("bold")
ax.set_title("Modalidade de Trabalho em TI no Brasil", pad=15)
plt.tight_layout()
plt.savefig("graficos/04_modalidade_trabalho.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Gráfico 4 salvo: graficos/04_modalidade_trabalho.png")

# ── 4. Insights finais ─────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("  INSIGHTS PRINCIPAIS")
print("=" * 55)

jr_dados  = df[(df["cargo"] == "Analista de Dados") & (df["senioridade"] == "Júnior")]["salario"].mean()
jr_ti     = df[(df["cargo"] == "Analista de TI")    & (df["senioridade"] == "Júnior")]["salario"].mean()
remoto_pct= (df["modalidade"] == "Remoto").mean() * 100
python_pct= df["Python"].mean() * 100

print(f"\n💡 Analista de Dados Júnior ganha em média R$ {jr_dados:,.0f}")
print(f"   vs Analista de TI Júnior: R$ {jr_ti:,.0f}")
print(f"   → Diferença de {((jr_dados/jr_ti)-1)*100:.0f}% a mais na área de dados\n")
print(f"💡 {remoto_pct:.0f}% das vagas de TI são remotas ou híbridas")
print(f"💡 Python está presente em {python_pct:.0f}% das vagas analisadas")
print(f"\n✅ Análise completa! Verifique a pasta 'graficos/' para os visuais.")
