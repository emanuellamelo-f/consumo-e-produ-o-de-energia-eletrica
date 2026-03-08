# ⚡ ENERGYX Dashboard (Streamlit)

Dashboard interativo para **monitoramento energético em tempo real** com Streamlit, incluindo:

- Simulação de consumo e produção por equipamentos (consumidores, produtores e prosumidores)
- Indicadores operacionais com visualizações dinâmicas
- Ranking de consumo e ocorrências
- Página extra com **cálculos de circuitos elétricos** (série e paralelo)

---

## 📌 Visão geral do projeto

Este projeto foi construído como um painel multipágina em Streamlit.

### Página principal (`app.py`)
Foco em monitoramento energético com atualização automática a cada 2 segundos.

Principais recursos:

1. **Simulação de ativos elétricos**
   - Consumidores: Geladeira, Ar Condicionado, Chuveiro, Iluminação, TV, Computador, Máquina de Lavar
   - Produtores: Painel Solar, Microturbina Eólica
   - Prosumidor: Bateria Residencial

2. **Medições instantâneas e acumuladas**
   - Potência de consumo e produção (W)
   - Energia acumulada (kWh)
   - Saldo energético e custo estimado por tarifa

3. **Indicadores visuais**
   - Gauge de OEE energético (Disponibilidade × Performance × Qualidade)
   - Séries temporais de produção e consumo
   - Ranking dos maiores consumidores
   - Ranking de ocorrências por ativo

4. **Controles de operação**
   - Nome do cliente
   - Localização
   - Tarifa de energia (R$/kWh)
   - Filtro por mês para gráfico temporal
   - Botão para zerar medições

5. **Interface personalizada**
   - Tema escuro customizado via CSS
   - Cabeçalho nativo do Streamlit ocultado para aparência mais limpa

---

### Página secundária (`pages/2_Calculos_Circuitos_Eletricos.py`)
Módulo educacional/prático de circuitos elétricos.

Conteúdo e funcionalidades:

- Resumo das fórmulas:
  - Lei de Ohm: $V = R \cdot I$
  - Potência: $P = V \cdot I = I^2R = \frac{V^2}{R}$
  - Energia: $E(kWh)=\frac{P(W)}{1000}\cdot t(h)$
- Simulador de circuito em **Série** e **Paralelo**
- Entrada de resistências por lista (ex.: `10, 20, 40`)
- Cálculo de:
  - Resistência equivalente
  - Corrente total
  - Potência total
  - Energia no período
- Tabela detalhada por elemento (R1, R2, ...)
- Conferências automáticas de consistência (soma de tensões/correntes)

---

## 🧠 Lógica de simulação (página principal)

A simulação é baseada em potência nominal por equipamento com variação aleatória:

- Cada ativo possui `base_w` e fator de variação `var`
- Em cada atualização, a função gera novos valores de consumo/produção
- O acumulado em kWh é calculado por:

$$
E = \frac{P \cdot \Delta t}{1000}
$$

onde $P$ está em watts e $\Delta t$ em horas.

### Regras importantes implementadas

- **Auto-refresh**: a cada 2000 ms
- **Consumo instantâneo total limitado a 15 kW** (regra de segurança visual da simulação)
- Histórico mantido em `st.session_state` sem truncamento temporal
- Custo calculado apenas quando consumo supera produção:

$$
\text{custo} = \max(0, \text{consumo} - \text{produção}) \cdot \text{tarifa}
$$

---

## 🗂️ Estrutura do projeto

- `app.py` → aplicação principal do dashboard
- `pages/2_Calculos_Circuitos_Eletricos.py` → página extra de cálculos elétricos
- `requirements.txt` → dependências Python
- `dados_roupas.csv` → arquivo de dados tabulares (não utilizado na lógica atual do dashboard)

---

## ✅ Requisitos

- Python 3.10+ (recomendado)
- `pip`
- Ambiente virtual (recomendado)

Dependências do projeto:

- streamlit
- streamlit-autorefresh
- pandas
- plotly
- numpy

---

## 🚀 Como executar

1. Abra a pasta do projeto no terminal.
2. Crie e ative um ambiente virtual.
3. Instale as dependências.
4. Execute o Streamlit.

Comandos (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Após iniciar, acesse no navegador o endereço local exibido pelo Streamlit (normalmente `http://localhost:8501`).

---

## 📊 Indicadores presentes no dashboard

### OEE Energético
Calculado como:

$$
OEE = \frac{Disponibilidade \times Performance \times Qualidade}{10000}
$$

Com os três termos em percentual (0–100).

### Produção vs Consumo (tempo)
Gráfico de linha com:

- Produção (kW)
- Consumo (kW)
- Filtro mensal para análise de período

### Ranking de consumo
Barra horizontal dos principais ativos com maior potência de consumo.

### Ranking de ocorrências
Pontuação por ativo com base em regras simples de alerta:

- Potência de consumo > 1000 W
- Saldo energético negativo
- Custo acima da mediana dos custos

---

## 🛠️ Personalização rápida

Você pode ajustar facilmente no código:

- Lista de ativos e parâmetros (`APARELHOS`) no `app.py`
- Meta diária (`meta_dia_kwh`)
- Intervalo de atualização (`st_autorefresh`)
- Escalas e limites de gráficos Plotly
- Faixa de tarifa no slider da sidebar

---

## ⚠️ Observações técnicas

- O projeto usa dados **simulados** para fins de visualização e análise.
- Os números não representam medição física real de sensores.
- O reset de medição limpa o `session_state` e reinicia os acumulados.

---

## 💡 Próximas melhorias sugeridas

- Persistência de histórico em banco de dados
- Integração com API/IoT para dados reais
- Exportação de relatórios (CSV/PDF)
- Alertas automáticos (e-mail/WhatsApp)
- Página de circuitos mistos (série + paralelo)

---

## 👤 Autor

Projeto desenvolvido para fins de monitoramento e estudo de energia elétrica com Streamlit.

Se quiser, posso também criar uma versão do README com **badges**, **GIF da interface** e seção de **deploy (Streamlit Community Cloud)**.