# ⚡ ENERGYX: Gestão e Simulação Energética

O **ENERGYX** é um ecossistema interativo desenvolvido em Python para monitoramento de ativos elétricos e cálculos de circuitos em tempo real.

## 🎯 O que o projeto oferece?

### 1. Dashboard de Monitoramento (`app.py`)

Painel dinâmico que simula o comportamento elétrico de uma residência ou indústria.

* **Simulação Realista:** Gerencia 10 ativos (Geladeira, Painel Solar, Baterias, etc.) com variações aleatórias.
* **Métricas OEE:** Mede Disponibilidade, Performance e Qualidade do sistema energético.
* **Análise Financeira:** Calcula custos e saldo energético (Produção vs. Consumo) instantaneamente.
* **Interface Live:** Atualização automática a cada 2 segundos com gráficos interativos.

### 2. Calculadora de Circuitos (`pages/2_Calculos.py`)

Módulo técnico-educativo para análise de redes elétricas.

* **Associações:** Suporte completo para circuitos em **Série** e **Paralelo**.
* **Leis de Ohm e Kirchhoff:** Cálculos automáticos de Resistência Equivalente ($R_{eq}$), Corrente ($I$) e Potência ($P$).
* **Detalhamento:** Gera tabelas individuais por componente para análise de queda de tensão.

---

## 🛠️ Tecnologia e Lógica

A aplicação utiliza **Streamlit** para a interface e **Plotly** para visualização de dados. A base do cálculo energético segue a fórmula:

$$E(kWh) = \frac{P(W) \cdot \Delta t(h)}{1000}$$

*Onde $P$ é a potência instantânea e $\Delta t$ o intervalo de tempo da simulação.*

---

## 🚀 Como Executar

### **Windows (Mais rápido)**

Dê um clique duplo no arquivo **`Abrir Dashboard.vbs`**. Ele configura o ambiente e abre o app automaticamente.

### **Qualquer Sistema (Terminal)**

1. Instale as dependências: `pip install -r requirements.txt`
2. Rode o app: `streamlit run app.py`

---

## 🌐 Deploy (Colocar Online)

O projeto está pronto para o **Streamlit Community Cloud**:

1. Suba os arquivos para um repositório no **GitHub**.
2. Conecte o repositório em [share.streamlit.io](https://share.streamlit.io).
3. Clique em **Deploy** e receba sua URL pública.

---

## 📋 Requisitos do Sistema

* **Linguagem:** Python 3.10+
* **Bibliotecas:** `streamlit`, `pandas`, `plotly`, `numpy`, `streamlit-autorefresh`.

---

## 📁 Estrutura do Projeto

```
dashboard/
│
├── app.py                              # Dashboard principal
├── pages/
│   └── 2_Calculos_Circuitos_Eletricos.py  # Módulo de cálculos
├── requirements.txt                    # Dependências
├── runtime.txt                         # Versão Python (deploy)
├── Abrir Dashboard.vbs                 # Launcher Windows
├── INICIAR.bat                         # Alternativa launcher
├── INICIAR.ps1                         # Launcher PowerShell
└── .streamlit/
    └── config.toml                     # Configuração Streamlit

```

---

## 📊 Principais Funcionalidades

### Dashboard Principal

- **Cards de métricas** com meta diária, produção e compra da rede
- **Gauge OEE energético** (indicador visual 0-100%)
- **Gráficos de tendência** (Disponibilidade, Performance, Qualidade)
- **Rankings interativos** de consumo e ocorrências
- **Gráficos temporais** de produção vs consumo

### Calculadora de Circuitos

- **Simulador série/paralelo** com entrada de resistências
- **Cálculos automáticos** de $R_{eq}$, $I$, $P$, $E$
- **Tabela detalhada** por componente
- **Validação automática** das Leis de Kirchhoff

---

## 🎨 Interface

- **Tema escuro** customizado via CSS
- **Auto-refresh** a cada 2 segundos
- **Gráficos interativos** com zoom e hover
- **Sidebar** com controles de cliente, localização e tarifa

---

## 🔧 Personalização

Você pode ajustar no código:

- Lista de ativos e parâmetros (`APARELHOS` no `app.py`)
- Meta diária de energia (`meta_dia_kwh`)
- Intervalo de atualização (`st_autorefresh`)
- Escalas e limites dos gráficos Plotly
- Faixa de tarifa no slider

---

## 📈 Roadmap Futuro

- **Conexão IoT:** Integração com sensores ESP32/Arduino
- **IA Preditiva:** Previsão de consumo mensal via Machine Learning
- **Relatórios:** Exportação automática de PDFs mensais
- **Alertas:** Notificações por e-mail/WhatsApp

---

## 👤 Autor

Projeto desenvolvido para fins de monitoramento e estudo de energia elétrica com Streamlit.

---

## 📖 Como Usar

### 🚀 Abertura Rápida (Windows)

1. Localize o arquivo `Abrir Dashboard.vbs` na pasta do projeto
2. Clique duplo no arquivo
3. Aguarde 6 segundos - o dashboard abrirá automaticamente no navegador
4. Pronto! Interface do ENERGYX estará visível

### 🎯 O Que Você Verá

#### Tela Principal
- Cards com métricas de energia
- Gauge OEE (velocímetro 0-100%)
- Gráficos de tendência temporal
- Rankings de consumo e alertas

#### Menu Lateral
- Nome do cliente e localização
- Tarifa de energia (R$/kWh)
- Filtro mensal
- Botão "Zerar medição"

#### Página 2 - Cálculos
1. No menu lateral, clique em "Cálculos de Circuitos Elétricos"
2. Escolha: Série ou Paralelo
3. Informe tensão (ex: 220V)
4. Digite resistências (ex: `10, 20, 40`)
5. Veja cálculos automáticos

---

## 📱 Acesso Remoto (Rede Local)

1. Após abrir o dashboard, veja o terminal
2. Procure o **Network URL** (ex: `http://192.168.0.4:8501`)
3. Digite esse endereço em outro dispositivo na mesma rede

---

## ❓ Solução de Problemas

**Dashboard não abre?**
- Verifique se Python está instalado
- Confirme que a pasta `.venv` existe
- Execute `INICIAR.bat` para ver erros

**Página não carrega?**
- Aguarde até 10 segundos na primeira execução
- Verifique se a porta 8501 está livre

**Como parar?**
- Feche a aba do navegador
- Finalize processos "python" ou "streamlit" no Gerenciador de Tarefas

O projeto é dividido em duas frentes principais:

### 1. Central de Monitoramento (app.py)

Um painel dinâmico que simula o comportamento de uma residência ou pequena indústria inteligente.

- **Ecossistema Completo**: Simula consumidores (ar-condicionado, chuveiro), produtores (painel solar, eólica) e prosumidores (baterias).
- **Inteligência Industrial (OEE)**: Adaptamos o índice Overall Equipment Effectiveness para a energia, medindo Disponibilidade, Performance e Qualidade do seu sistema.
- **Visão Financeira**: Cálculo instantâneo de gastos baseados na tarifa configurável (R$/kWh).
- **Atualização Ativa**: Os dados renovam-se a cada 2 segundos, criando uma experiência de monitoramento "ao vivo".

### 2. Laboratório de Cálculos (Calculos_Circuitos_Eletricos.py)

Um módulo educativo e prático para engenheiros e estudantes.

- **Simulador de Circuitos**: Calcule associações em série e paralelo apenas digitando as resistências.
- **Detalhamento Técnico**: Tabela completa com queda de tensão e corrente individual para cada componente.
- **Validação Automática**: O sistema confere se as Leis de Kirchhoff estão sendo respeitadas.

### 🛠️ Por dentro da tecnologia

O "cérebro" do dashboard utiliza lógica matemática para simular o mundo real:

- **Variação Estocástica**: Cada equipamento possui uma potência base que oscila aleatoriamente para simular o uso real.
- **Cálculo de Energia**: Utilizamos a integração da potência no tempo para chegar ao valor de consumo:

$$E(kWh) = \frac{P(W) \cdot \Delta t(h)}{1000}$$

- **Gestão de Estado**: O histórico é preservado via `st.session_state`, permitindo que os gráficos de linha mostrem a evolução dos dados sem recarregar a página.

### 📦 Como instalar e rodar

**No Windows (O jeito fácil)**

Basta dar um clique duplo no arquivo `Abrir Dashboard.vbs`. Ele configurará o ambiente e abrirá o navegador silenciosamente para você.

**Via Terminal (Qualquer SO)**

1. Instale as dependências: `pip install -r requirements.txt`
2. Inicie a aplicação: `streamlit run app.py`

### 🌐 Deploy: Leve seu Dashboard para o Mundo

O ENERGYX já está preparado para nuvem! Como o GitHub Pages não suporta Python, recomendamos o **Streamlit Community Cloud**:

1. Suba seu código para um repositório no GitHub.
2. Conecte sua conta em [share.streamlit.io](https://share.streamlit.io).
3. Selecione seu repositório e clique em **Deploy**.
4. Voilá! Você terá um link público (ex: `energyx.streamlit.app`) para acessar de qualquer lugar.

### 📈 Futuro do Projeto

- **Conexão IoT**: Substituir a simulação por dados reais de sensores (ESP32/Arduino).
- **Previsão com IA**: Integrar modelos de Machine Learning para prever o consumo do próximo mês.
- **Relatórios**: Exportação automática de PDFs com o fechamento mensal de custos.

---

## �📌 Visão geral do projeto

O projeto foi construído como um painel multipágina em Streamlit.

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

### Método 1: Executar com um clique (Windows)

**Mais fácil:** dê clique duplo em um dos arquivos abaixo:

- **`Abrir Dashboard.vbs`** ⭐ (recomendado - abre silenciosamente sem terminal)
- **`INICIAR.bat`** (abre com janela de terminal)
- **`INICIAR.ps1`** (PowerShell com janela)

O aplicativo abrirá automaticamente no seu navegador padrão em `http://localhost:8501`

### Método 2: Terminal (qualquer sistema operacional)

PowerShell/CMD (Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Linux/Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Após iniciar, acesse no navegador o endereço local exibido pelo Streamlit (normalmente `http://localhost:8501`).

### Execução no GitHub Codespaces (opcional)

Se abrir o projeto no Codespaces, execute:

```bash
pip install -r requirements.txt
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 📦 Publicar no GitHub

1. Crie um repositório vazio no GitHub.
2. No projeto local, execute:

```bash
git init
git add .
git commit -m "feat: initial version of ENERGYX dashboard"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

3. Confirme no GitHub se os arquivos `app.py`, `pages/`, `requirements.txt` e `README.md` foram enviados.

---

## 🌐 Colocar no ar como site (Streamlit Community Cloud)

Este projeto é Streamlit, então o caminho mais simples para virar site é o Streamlit Community Cloud.

> **Importante:** GitHub Pages não executa aplicações Python/Streamlit no servidor.
> O GitHub hospeda o código; a execução web do app deve ser feita em um serviço como Streamlit Community Cloud.

### Pré-requisitos

- Repositório no GitHub com os arquivos do projeto
- Arquivo principal: `app.py`
- Dependências em `requirements.txt`

### Passo a passo

1. Acesse https://share.streamlit.io
2. Faça login com sua conta GitHub.
3. Clique em **Create app**.
4. Selecione:
   - **Repository**: seu repositório
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Clique em **Deploy**.

Em poucos minutos, o app ficará online com uma URL pública no formato:

`https://seu-app.streamlit.app`

### Arquivos já preparados para deploy

- `requirements.txt` (dependências)
- `runtime.txt` (versão do Python)
- `.streamlit/config.toml` (configuração de execução)
- `.github/workflows/ci.yml` (validação automática a cada push/PR)

### Checklist final

- [ ] Repositório publicado no GitHub
- [ ] Branch principal: `main`
- [ ] Deploy criado em `share.streamlit.io` apontando para `app.py`
- [ ] Aplicação abrindo via URL pública

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

---

## 📖 Guia Rápido - Como Abrir o Dashboard

### 🚀 Forma Mais Simples (Windows)

1. **Localize o arquivo** `Abrir Dashboard.vbs` na pasta do projeto
2. **Clique duplo** no arquivo
3. **Aguarde 6 segundos** - o dashboard abrirá automaticamente no navegador
4. **Pronto!** Você verá a interface do ENERGYX Dashboard

### 🎯 O Que Você Verá no Dashboard

#### Tela Principal (Página 1)
- **Cards no topo**: Meta diária, Produção no dia, Compra da rede
- **Gráfico OEE**: Indicador em formato de velocímetro (0-100%)
- **Gráficos de tendência**: Disponibilidade, Performance e Qualidade
- **Ranking de consumo**: Barra horizontal dos equipamentos que mais consomem
- **Gráfico temporal**: Produção vs Consumo ao longo do tempo
- **Ranking de ocorrências**: Alertas por equipamento

#### Menu Lateral (Sidebar)
- **Nome do cliente**: Personalize o nome
- **Localização**: Defina a localização
- **Tarifa de energia**: Ajuste o valor em R$/kWh
- **Filtro de mês**: Selecione o período para análise
- **Botão "Zerar medição"**: Reinicia todos os dados

#### Página 2 - Cálculos Elétricos
1. No menu lateral, clique em **"Cálculos de Circuitos Elétricos"**
2. Escolha o tipo: **Série** ou **Paralelo**
3. Informe a tensão da fonte (ex: 220V)
4. Digite as resistências separadas por vírgula (ex: `10, 20, 40`)
5. Veja os cálculos automáticos:
   - Resistência equivalente
   - Corrente total
   - Potência total
   - Energia consumida
   - Tabela detalhada por resistor

### 🔧 Controles Úteis

**Durante o uso:**
- O dashboard **atualiza sozinho** a cada 2 segundos
- Não precisa recarregar a página manualmente
- Para **parar**, feche a aba do navegador

**Para abrir novamente:**
- Clique duplo em `Abrir Dashboard.vbs` novamente
- Se já estiver rodando, só abrirá uma nova aba do navegador

### ⚡ Funções do Dashboard Explicadas

#### 1. **Simulação de Ativos Elétricos**
Simula 10 equipamentos diferentes:
- **Consumidores** (7): Geladeira, Ar Condicionado, Chuveiro, etc.
- **Produtores** (2): Painel Solar, Microturbina Eólica
- **Prosumidor** (1): Bateria (pode consumir ou produzir)

Cada um tem potência base e variação aleatória para simular uso real.

#### 2. **Medições em Tempo Real**
- **Potência instantânea** (W): Quanto está consumindo/produzindo AGORA
- **Energia acumulada** (kWh): Total desde que iniciou
- **Saldo energético**: Produção - Consumo
- **Custo**: Calculado pela tarifa quando consome mais que produz

#### 3. **Indicador OEE Energético**
Métrica industrial adaptada para energia:
- **Disponibilidade**: Sistema está gerando energia?
- **Performance**: Quanto está gerando vs capacidade máxima
- **Qualidade**: Quão equilibrado está consumo vs produção

#### 4. **Gráficos Interativos**
- **Hover**: Passe o mouse para ver valores exatos
- **Zoom**: Clique e arraste para ampliar áreas
- **Reset**: Clique duplo para voltar à visualização original

#### 5. **Calculadora de Circuitos**
Ferramenta educacional para:
- Calcular resistência equivalente (série/paralelo)
- Ver tensão e corrente em cada componente
- Calcular potência e energia consumida
- Validar resultados automaticamente

### 📱 Acessar de Outros Dispositivos

Se quiser abrir em outro computador/celular na mesma rede:

1. Após abrir o dashboard, veja o terminal (se usar INICIAR.bat)
2. Procure o **Network URL** (ex: `http://192.168.0.4:8501`)
3. Digite esse endereço no navegador de outro dispositivo
4. Acesse remotamente pela rede local

### 🌐 Publicar na Internet

Para acessar de qualquer lugar:

1. Envie o projeto para o GitHub
2. Acesse https://share.streamlit.io
3. Conecte com sua conta GitHub
4. Selecione o repositório e clique em Deploy
5. Receba uma URL pública (ex: `https://seu-app.streamlit.app`)

### ❓ Solução de Problemas

**O dashboard não abre?**
- Verifique se o Python está instalado
- Confirme que o ambiente virtual existe (pasta `.venv`)
- Tente executar `INICIAR.bat` para ver mensagens de erro

**Página não carrega?**
- Aguarde até 10 segundos na primeira execução
- Verifique se a porta 8501 não está em uso
- Reinicie o computador se necessário

**Quer parar o dashboard?**
- Feche todas as abas do navegador com o dashboard
- Abra o Gerenciador de Tarefas e finalize processos "python" ou "streamlit"