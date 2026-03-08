import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from streamlit_autorefresh import st_autorefresh


st.set_page_config(
    page_title="⚡ ENERGYX - Central de Monitoramento Inteligente",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ocultar elementos do cabeçalho do Streamlit
st.markdown(
    """
    <style>
    /* Ocultar cabeçalho padrão do Streamlit */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    /* Ocultar toolbar */
    div[data-testid="stToolbar"] {
        display: none;
    }
    
    /* Ocultar menu hamburger */
    button[kind="header"] {
        display: none;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 10%, #1a2347 0%, #0b1228 45%, #080d1f 100%);
        color: #f0f4ff;
    }
    .main-title {
        color: #f8fbff;
        text-align: left;
        font-size: 1.9rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        text-align: left;
        color: #8ca2e6;
        margin-bottom: 1rem;
        font-size: 0.92rem;
    }
    .card {
        background: linear-gradient(180deg, rgba(24,35,77,0.88) 0%, rgba(16,24,53,0.88) 100%);
        border: 1px solid rgba(120, 150, 255, 0.18);
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 10px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.2);
    }
    .card-title {
        font-size: 0.85rem;
        color: #9eb4ff;
        margin-bottom: 4px;
    }
    .card-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f7fbff;
    }
    .small-note {
        font-size: 0.8rem;
        color: #8aa2ef;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if 'update_key' not in st.session_state:
    st.session_state.update_key = 0

APARELHOS = [
    {"nome": "Geladeira", "tipo": "consumidor", "base_w": 180, "var": 0.35},
    {"nome": "Ar Condicionado", "tipo": "consumidor", "base_w": 1450, "var": 0.40},
    {"nome": "Chuveiro", "tipo": "consumidor", "base_w": 3800, "var": 0.60},
    {"nome": "Iluminação", "tipo": "consumidor", "base_w": 420, "var": 0.25},
    {"nome": "TV", "tipo": "consumidor", "base_w": 130, "var": 0.30},
    {"nome": "Computador", "tipo": "consumidor", "base_w": 300, "var": 0.35},
    {"nome": "Máquina de Lavar", "tipo": "consumidor", "base_w": 900, "var": 0.55},
    {"nome": "Painel Solar", "tipo": "produtor", "base_w": 2400, "var": 0.45},
    {"nome": "Microturbina Eólica", "tipo": "produtor", "base_w": 1100, "var": 0.50},
    {"nome": "Bateria Residencial", "tipo": "prosumidor", "base_w": 900, "var": 0.70},
]

APARELHOS_ORDEM_FIXA = [a["nome"] for a in APARELHOS]
TOP6_FIXO = [a["nome"] for a in sorted(APARELHOS, key=lambda x: x["base_w"], reverse=True)[:6]]


def inicializar_estado():
    if "acumulado" not in st.session_state:
        st.session_state.acumulado = pd.DataFrame(
            {
                "aparelho": [a["nome"] for a in APARELHOS],
                "tipo": [a["tipo"] for a in APARELHOS],
                "consumo_kwh": 0.0,
                "producao_kwh": 0.0,
                "potencia_consumo_w": 0.0,
                "potencia_producao_w": 0.0,
            }
        )

    if "historico" not in st.session_state:
        st.session_state.historico = pd.DataFrame(
            columns=["timestamp", "consumo_kw", "producao_kw", "saldo_kw"]
        )

    if "last_update" not in st.session_state:
        st.session_state.last_update = datetime.now()


def gerar_potencia(aparelho):
    ruido = np.random.normal(aparelho["base_w"], aparelho["base_w"] * aparelho["var"])

    if aparelho["tipo"] == "consumidor":
        consumo_w = max(0.0, ruido)
        producao_w = 0.0

    elif aparelho["tipo"] == "produtor":
        producao_w = max(0.0, ruido)
        consumo_w = np.random.uniform(10, 60)

    else:  # prosumidor (bateria pode carregar ou descarregar)
        fluxo = np.random.normal(0, aparelho["base_w"])
        if fluxo >= 0:
            producao_w = fluxo
            consumo_w = np.random.uniform(30, 80)
        else:
            producao_w = 0.0
            consumo_w = abs(fluxo) + np.random.uniform(30, 80)

    return consumo_w, producao_w


def atualizar_medicoes(dt_horas):
    acumulado = st.session_state.acumulado.copy()

    for i, ap in enumerate(APARELHOS):
        consumo_w, producao_w = gerar_potencia(ap)

        acumulado.loc[i, "potencia_consumo_w"] = consumo_w
        acumulado.loc[i, "potencia_producao_w"] = producao_w
        acumulado.loc[i, "consumo_kwh"] += (consumo_w * dt_horas) / 1000
        acumulado.loc[i, "producao_kwh"] += (producao_w * dt_horas) / 1000

    consumo_kw_total = acumulado["potencia_consumo_w"].sum() / 1000
    producao_kw_total = acumulado["potencia_producao_w"].sum() / 1000
    
    # Limitar consumo a no máximo 15 kW
    consumo_kw_total = min(consumo_kw_total, 15.0)
    
    saldo_kw = producao_kw_total - consumo_kw_total

    nova_linha = pd.DataFrame(
        [
            {
                "timestamp": datetime.now(),
                "consumo_kw": consumo_kw_total,
                "producao_kw": producao_kw_total,
                "saldo_kw": saldo_kw,
            }
        ]
    )

    if st.session_state.historico.empty:
        st.session_state.historico = nova_linha
    else:
        st.session_state.historico = pd.concat(
            [st.session_state.historico, nova_linha],
            ignore_index=True,
        )

    # Sem limite de tempo - mantém todo o histórico

    st.session_state.acumulado = acumulado


inicializar_estado()

# Auto-atualizar a cada 2 segundos
st_autorefresh(interval=2000, key="datarefresh")

with st.sidebar:
    st.header("⚙️ Configurações")
    cliente_nome = st.text_input("Nome do cliente", value="Cliente Alpha")
    cliente_localizacao = st.text_input("Localização", value="São Paulo - SP")
    tarifa = st.slider("Tarifa de energia (R$/kWh)", 0.30, 2.50, 0.95, 0.05)

    if st.button("🔄 Zerar medição"):
        st.session_state.clear()
        st.rerun()

# Atualizar dados automaticamente a cada refresh
agora = datetime.now()
dt_horas = max((agora - st.session_state.last_update).total_seconds() / 3600, 1 / 3600)
st.session_state.last_update = agora
atualizar_medicoes(dt_horas)

df = st.session_state.acumulado.copy()
hist = st.session_state.historico.copy()

# Filtro de mês para o gráfico de produção ao longo do tempo
hist_plot = hist.copy()
if not hist_plot.empty:
    hist_plot["timestamp"] = pd.to_datetime(hist_plot["timestamp"])
    hist_plot["mes_ref"] = hist_plot["timestamp"].dt.strftime("%Y-%m")
    meses_disponiveis = sorted(hist_plot["mes_ref"].unique().tolist(), reverse=True)
else:
    meses_disponiveis = []

mes_selecionado = st.sidebar.selectbox(
    "Mês (gráfico de produção)",
    options=["Todos"] + meses_disponiveis,
    index=0,
)

if mes_selecionado != "Todos" and not hist_plot.empty:
    hist_plot = hist_plot[hist_plot["mes_ref"] == mes_selecionado].copy()

df["saldo_kwh"] = df["producao_kwh"] - df["consumo_kwh"]
df["custo_r$"] = (df["consumo_kwh"] - df["producao_kwh"]).clip(lower=0) * tarifa

# Garante estrutura completa no dataframe fixo (evita KeyError em custo_r$)
if "df_fixo" not in st.session_state:
    st.session_state.df_fixo = df.copy()

colunas_obrigatorias = [
    "aparelho",
    "tipo",
    "potencia_consumo_w",
    "potencia_producao_w",
    "consumo_kwh",
    "producao_kwh",
    "saldo_kwh",
    "custo_r$",
]

faltantes = [c for c in colunas_obrigatorias if c not in st.session_state.df_fixo.columns]
if faltantes:
    st.session_state.df_fixo = df.copy()

df_fixo = st.session_state.df_fixo


consumo_inst_kw = df["potencia_consumo_w"].sum() / 1000
producao_inst_kw = df["potencia_producao_w"].sum() / 1000
saldo_inst_kw = producao_inst_kw - consumo_inst_kw
autossuf = (producao_inst_kw / consumo_inst_kw * 100) if consumo_inst_kw > 0 else 0.0

hist_calc = hist.copy()
hist_calc["disp_pct"] = (hist_calc["producao_kw"] > 0.15).astype(float) * 100
hist_calc["disp_wh"] = hist_calc["producao_kw"] * 1000
hist_calc["perf"] = (
    (hist_calc["producao_kw"] / hist_calc["consumo_kw"].clip(lower=0.05)) * 100
).clip(0, 100)
hist_calc["qual"] = (
    (1 - (hist_calc["saldo_kw"].abs() / hist_calc["consumo_kw"].clip(lower=0.05))) * 100
).clip(0, 100)

janela = 30 if len(hist_calc) >= 30 else max(1, len(hist_calc))
disponibilidade = float(hist_calc["disp_pct"].tail(janela).mean()) if len(hist_calc) else 0.0
performance = float(hist_calc["perf"].tail(janela).mean()) if len(hist_calc) else 0.0
qualidade = float(hist_calc["qual"].tail(janela).mean()) if len(hist_calc) else 0.0

meta_dia_kwh = 180
energia_produzida_dia = df["producao_kwh"].sum()
energia_consumida_dia = df["consumo_kwh"].sum()
energia_rede_kwh = max(0.0, energia_consumida_dia - energia_produzida_dia)

# Criar estrutura sempre (necessário com auto-refresh)
st.markdown('<div class="main-title">⚡ ENERGYX • Central de Monitoramento Inteligente</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="sub-title">👤 Cliente: <b>{cliente_nome}</b> &nbsp;&nbsp;|&nbsp;&nbsp; 📍 Localização: <b>{cliente_localizacao}</b> &nbsp;&nbsp;|&nbsp;&nbsp; Última leitura: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</div>',
    unsafe_allow_html=True,
)

# Cards superiores
top1, top2, top3 = st.columns(3)

top1.markdown(
    '<div class="card"><div class="card-title">Meta diária</div><div class="card-value">180.0 kWh</div><div class="small-note">planejado</div></div>',
    unsafe_allow_html=True,
)

top2.markdown(
    f'<div class="card"><div class="card-title">Produção no dia</div><div class="card-value">{energia_produzida_dia:.1f} kWh</div><div class="small-note">gerado pelos ativos</div></div>',
    unsafe_allow_html=True,
)
top3.markdown(
    f'<div class="card"><div class="card-title">Compra da rede</div><div class="card-value">{energia_rede_kwh:.1f} kWh</div><div class="small-note">energia importada</div></div>',
    unsafe_allow_html=True,
)

# Linha 1 de gráficos
linha1_col1, linha1_col2, linha1_col3 = st.columns([1, 1.5, 1.5])

# Gráfico OEE em tempo real
linha1_col1.markdown("<div class='card-title'>OEE Energético</div>", unsafe_allow_html=True)
oee = (disponibilidade * performance * qualidade) / 10000
fig_oee = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=oee,
            number={"suffix": "%", "valueformat": ".1f"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#25c4dd"},
                "steps": [
                    {"range": [0, 60], "color": "#7f1d2d"},
                    {"range": [60, 80], "color": "#8a6d1f"},
                    {"range": [80, 100], "color": "#124c40"},
                ],
            },
        )
    )
fig_oee.update_layout(
    template="plotly_dark", 
    height=420, 
    margin=dict(l=10, r=10, t=35, b=10),
    uirevision="oee_fixo"
)
linha1_col1.plotly_chart(fig_oee, width="stretch")

# Gráficos de indicadores
linha1_col2.markdown("<div class='card-title'>Indicadores de Produção</div>", unsafe_allow_html=True)
indicador_df = hist_calc[["timestamp", "disp_wh", "perf", "qual"]].tail(60).copy()

for idx, (nome, campo, cor, unidade, eixo_max) in enumerate([
    ("Disponibilidade", "disp_wh", "#f4a261", " Wh", None),
    ("Performance", "perf", "#2a9dff", "%", 100),
    ("Qualidade", "qual", "#ff5f56", "%", 100),
]):
    fig_mini = go.Figure()
    fig_mini.add_trace(
        go.Scatter(
            x=indicador_df["timestamp"],
            y=indicador_df[campo],
            mode="lines",
            line=dict(color=cor, width=2),
            fill="tozeroy",
        fillcolor="rgba(255,255,255,0.02)",
            name=nome,
        )
    )
    fig_mini.update_layout(
        template="plotly_dark",
        height=130,
        margin=dict(l=5, r=5, t=28, b=8),
        title=f"{nome}: {indicador_df[campo].iloc[-1]:.1f}{unidade}",
        xaxis=dict(showgrid=False, visible=False, fixedrange=True),
        yaxis=dict(range=[0, eixo_max] if eixo_max else None, showgrid=False, visible=False, fixedrange=True),
        showlegend=False,
        uirevision=f"ind_{campo}"
    )
    linha1_col2.plotly_chart(fig_mini, width="stretch")

# Ranking de consumo
linha1_col3.markdown("<div class='card-title'>Ranking de maior consumo (clique para ver cálculos)</div>", unsafe_allow_html=True)
ranking_cons = (
    df_fixo[df_fixo["aparelho"].isin(TOP6_FIXO)]
    .set_index("aparelho")
    .reindex(TOP6_FIXO)
    .reset_index()
)

aparelho_sel = linha1_col3.selectbox(
        "Selecione um aparelho:",
        options=ranking_cons["aparelho"].tolist(),
        key="select_aparelho_consumo",
    )
    
if aparelho_sel:
    dados_ap = df_fixo[df_fixo["aparelho"] == aparelho_sel].iloc[0]
    
    tensao_v = 220
    corrente_a = dados_ap["potencia_consumo_w"] / tensao_v
    energia_kwh_dia = dados_ap["consumo_kwh"]
    custo_dia = dados_ap["custo_r$"]
    
    calc_html = f"<div style='font-size:0.9rem;padding:8px;background:rgba(30,40,80,0.6);border-radius:8px;margin:8px 0;'>"
    calc_html += f"<strong>📊 {aparelho_sel}</strong><br>"
    calc_html += f"- Potência: $P = {dados_ap['potencia_consumo_w']:.2f}$ W<br>"
    calc_html += f"- Corrente: $I = {corrente_a:.3f}$ A<br>"
    calc_html += f"- Resistência: $R = {tensao_v/corrente_a:.1f}$ Ω<br>"
    calc_html += f"- Energia: $E = {energia_kwh_dia:.3f}$ kWh<br>"
    calc_html += f"- Custo: R$ {custo_dia:.2f}<br>"
    
    if dados_ap["potencia_producao_w"] > 0:
        calc_html += f"- Produção: {dados_ap['potencia_producao_w']:.1f} W<br>"
    calc_html += "</div>"
    
    linha1_col3.markdown(calc_html, unsafe_allow_html=True)

fig_rank_cons = px.bar(
    ranking_cons,
    x="potencia_consumo_w",
    y="aparelho",
    orientation="h",
    text="potencia_consumo_w",
    color="potencia_consumo_w",
    color_continuous_scale="oranges",
    template="plotly_dark",
)
fig_rank_cons.update_traces(texttemplate="%{text:.0f} W", textposition="outside")
fig_rank_cons.update_layout(
    height=240, 
    margin=dict(l=140, r=60, t=15, b=15), 
    showlegend=False,
    yaxis=dict(tickfont=dict(size=11), categoryorder="array", categoryarray=TOP6_FIXO[::-1], fixedrange=True),
    xaxis=dict(title="Potência (W)", tickfont=dict(size=10), range=[0, 4500], fixedrange=True),
    uirevision="ranking_cons"
)
linha1_col3.plotly_chart(fig_rank_cons, width="stretch")

st.markdown("---")

# Linha 2 de gráficos
linha2_col1, linha2_col2 = st.columns([2, 1])

# Gráfico de produção ao longo do tempo
# Calcular totais do dia e mês
if not hist_plot.empty:
    hist_plot_calc = hist_plot.copy()
    hoje = datetime.now().date()
    hist_plot_calc["data"] = pd.to_datetime(hist_plot_calc["timestamp"]).dt.date
    hist_plot_calc["mes_atual"] = pd.to_datetime(hist_plot_calc["timestamp"]).dt.to_period('M')
    
    # Total do dia
    consumo_dia = hist_plot_calc[hist_plot_calc["data"] == hoje]["consumo_kw"].sum()
    producao_dia = hist_plot_calc[hist_plot_calc["data"] == hoje]["producao_kw"].sum()
    
    # Total do mês
    mes_atual = pd.Period(datetime.now(), freq='M')
    consumo_mes = hist_plot_calc[hist_plot_calc["mes_atual"] == mes_atual]["consumo_kw"].sum()
    producao_mes = hist_plot_calc[hist_plot_calc["mes_atual"] == mes_atual]["producao_kw"].sum()
    
    titulo_grafico = f"Produção ao longo do tempo | Dia: {producao_dia:.2f} kW / {consumo_dia:.2f} kW | Mês: {producao_mes:.2f} kW / {consumo_mes:.2f} kW"
else:
    titulo_grafico = "Produção ao longo do tempo"

linha2_col1.markdown(f"<div class='card-title'>{titulo_grafico}</div>", unsafe_allow_html=True)
fig_linha = go.Figure()
fig_linha.add_trace(
    go.Scatter(
        x=hist_plot["timestamp"],
        y=hist_plot["producao_kw"],
        mode="lines+markers",
        name="Produção",
        line=dict(color="#dbe8ff", width=3, shape='spline'),
        marker=dict(size=4),
    )
)
fig_linha.add_trace(
    go.Scatter(
        x=hist_plot["timestamp"],
        y=hist_plot["consumo_kw"],
        mode="lines",
        name="Consumo",
        line=dict(color="#ff5f56", width=2, dash="dot", shape='spline'),
    )
)
fig_linha.update_layout(
    template="plotly_dark",
    height=350,
    margin=dict(l=50, r=20, t=20, b=40),
    legend=dict(orientation="h", y=1.08, x=0),
    xaxis=dict(title="Timestamp", tickangle=0, fixedrange=True),
    yaxis=dict(title="Potência (kW)", range=[0, 15], fixedrange=True),
    uirevision="prod_linha"
)
linha2_col1.plotly_chart(fig_linha, width="stretch")

# Gráfico de ocorrências
linha2_col2.markdown("<div class='card-title'>Ranking de ocorrências reais</div>", unsafe_allow_html=True)
ocorr_df = df_fixo.copy()
ocorr_df["ocorrencias"] = (
    (ocorr_df["potencia_consumo_w"] > 1000).astype(int)
    + (ocorr_df["saldo_kwh"] < 0).astype(int)
    + (ocorr_df["custo_r$"] > ocorr_df["custo_r$"].median()).astype(int)
)
ocorr_df = (
    ocorr_df[["aparelho", "ocorrencias"]]
    .set_index("aparelho")
    .reindex(APARELHOS_ORDEM_FIXA)
    .reset_index()
)

fig_occ = px.bar(
    ocorr_df,
    x="aparelho",
    y="ocorrencias",
    color="ocorrencias",
    color_continuous_scale="sunset",
    template="plotly_dark",
)
fig_occ.update_layout(
    height=350, 
    margin=dict(l=40, r=20, t=20, b=80),
    xaxis=dict(title="Aparelho", tickangle=-45, tickfont=dict(size=10), categoryorder="array", categoryarray=APARELHOS_ORDEM_FIXA, fixedrange=True),
    yaxis=dict(title="Ocorrências", range=[0, 3], fixedrange=True),
    showlegend=False,
    uirevision="occ_chart"
)
linha2_col2.plotly_chart(fig_occ, width="stretch")

with st.expander("Verificação detalhada por aparelho"):
    df_exibir = df_fixo[
        [
            "aparelho",
            "tipo",
            "potencia_consumo_w",
            "potencia_producao_w",
            "consumo_kwh",
            "producao_kwh",
            "saldo_kwh",
            "custo_r$",
        ]
    ].copy()

    df_exibir = df_exibir.sort_values("saldo_kwh")
    df_exibir["potencia_consumo_w"] = df_exibir["potencia_consumo_w"].map(lambda x: f"{x:.0f} W")
    df_exibir["potencia_producao_w"] = df_exibir["potencia_producao_w"].map(lambda x: f"{x:.0f} W")
    df_exibir["consumo_kwh"] = df_exibir["consumo_kwh"].map(lambda x: f"{x:.3f}")
    df_exibir["producao_kwh"] = df_exibir["producao_kwh"].map(lambda x: f"{x:.3f}")
    df_exibir["saldo_kwh"] = df_exibir["saldo_kwh"].map(lambda x: f"{x:+.3f}")
    df_exibir["custo_r$"] = df_exibir["custo_r$"].map(lambda x: f"R$ {x:.2f}")
    st.dataframe(df_exibir, use_container_width=True, hide_index=True, height=400)

consumidores_criticos = df_fixo.sort_values("consumo_kwh", ascending=False).head(3)["aparelho"].tolist()
st.info("Pontos de atenção: " + ", ".join(consumidores_criticos))
