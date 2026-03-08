import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cálculos de Circuitos Elétricos", page_icon="🔌", layout="wide")

st.title("🔌 Cálculos de Circuitos Elétricos")
st.caption("Resumo prático da soma de circuitos em série e em paralelo")

st.markdown("""
### 1) Leis básicas usadas

- **Lei de Ohm:** $V = R \cdot I$
- **Potência elétrica:** $P = V \cdot I = I^2R = \frac{V^2}{R}$
- **Energia consumida/gerada:** $E(kWh)=\frac{P(W)}{1000}\cdot t(h)$

### 2) Soma em série

Em série, a **corrente é a mesma** em todos os elementos:

$$I_1 = I_2 = ... = I_n = I_{total}$$

A resistência equivalente é:

$$R_{eq} = R_1 + R_2 + ... + R_n$$

A tensão total é a soma das quedas:

$$V_{total} = V_1 + V_2 + ... + V_n$$

### 3) Soma em paralelo

Em paralelo, a **tensão é a mesma** em todos os ramos:

$$V_1 = V_2 = ... = V_n = V_{total}$$

A resistência equivalente é:

$$\frac{1}{R_{eq}} = \frac{1}{R_1} + \frac{1}{R_2} + ... + \frac{1}{R_n}$$

A corrente total é a soma das correntes dos ramos:

$$I_{total} = I_1 + I_2 + ... + I_n$$
""")

st.divider()
st.subheader("🧮 Simulador de soma de circuitos")

col1, col2, col3, col4 = st.columns(4)
with col1:
    tipo = st.selectbox("Tipo de ligação", ["Série", "Paralelo"])
with col2:
    tensao_fonte = st.number_input("Tensão da fonte (V)", min_value=1.0, value=220.0, step=1.0)
with col3:
    tempo_h = st.number_input("Tempo de uso (h)", min_value=0.1, value=1.0, step=0.1)
with col4:
    resist_str = st.text_input("Resistências (ohms)", value="10, 20, 40")

try:
    resistencias = [float(x.strip()) for x in resist_str.split(",") if x.strip()]
except ValueError:
    st.error("Digite as resistências separadas por vírgula, por exemplo: 10, 20, 40")
    st.stop()

if not resistencias:
    st.warning("Informe pelo menos uma resistência.")
    st.stop()

if any(r <= 0 for r in resistencias):
    st.error("Todas as resistências devem ser maiores que zero.")
    st.stop()

if tipo == "Série":
    r_eq = sum(resistencias)
    i_total = tensao_fonte / r_eq
    p_total = tensao_fonte * i_total

    linhas = []
    for i, r in enumerate(resistencias, start=1):
        i_i = i_total
        v_i = i_i * r
        p_i = v_i * i_i
        linhas.append(
            {
                "Elemento": f"R{i}",
                "R (Ω)": r,
                "V_i (V)": v_i,
                "I_i (A)": i_i,
                "P_i (W)": p_i,
            }
        )

else:  # Paralelo
    inv = sum(1 / r for r in resistencias)
    r_eq = 1 / inv
    i_total = tensao_fonte / r_eq
    p_total = tensao_fonte * i_total

    linhas = []
    for i, r in enumerate(resistencias, start=1):
        v_i = tensao_fonte
        i_i = v_i / r
        p_i = v_i * i_i
        linhas.append(
            {
                "Elemento": f"R{i}",
                "R (Ω)": r,
                "V_i (V)": v_i,
                "I_i (A)": i_i,
                "P_i (W)": p_i,
            }
        )

df = pd.DataFrame(linhas)
energia_kwh = (p_total / 1000) * tempo_h

k1, k2, k3, k4 = st.columns(4)
k1.metric("Resistência equivalente", f"{r_eq:.4f} Ω")
k2.metric("Corrente total", f"{i_total:.4f} A")
k3.metric("Potência total", f"{p_total:.2f} W")
k4.metric("Energia no período", f"{energia_kwh:.4f} kWh")

st.dataframe(df.style.format({"R (Ω)": "{:.4f}", "V_i (V)": "{:.4f}", "I_i (A)": "{:.4f}", "P_i (W)": "{:.4f}"}), width="stretch")

st.markdown("### ✅ Conferências automáticas")
if tipo == "Série":
    soma_tensao = df["V_i (V)"].sum()
    st.write(f"- Soma das tensões dos elementos: **{soma_tensao:.4f} V** (deve ser ≈ tensão da fonte: **{tensao_fonte:.4f} V**) ")
    st.write(f"- Corrente em todos os elementos: **{df['I_i (A)'].iloc[0]:.4f} A**")
else:
    soma_corrente = df["I_i (A)"].sum()
    st.write(f"- Soma das correntes dos ramos: **{soma_corrente:.4f} A** (deve ser ≈ corrente total: **{i_total:.4f} A**) ")
    st.write(f"- Tensão em todos os ramos: **{tensao_fonte:.4f} V**")

st.info("Se quiser, eu também posso adicionar uma página de circuitos mistos (série + paralelo) com diagrama e cálculo passo a passo.")
