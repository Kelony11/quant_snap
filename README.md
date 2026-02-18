# QuantSnap 📊🌐 

A `Python` toolkit that downloads historical market data from `Yahoo Finance`, generates basic market analytics, 
simple strategy backtest, and serves **precomputed** results in a `Flask` dashboard.

> **Disclaimer:** Educational use only. Not investment advice.

---

## Requirements 🧱
- `Python` 3.10+
- `Flask` 3.1.2+

---

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the analysis (generates files) 📈📉

1. **Download data (CSV)**
    ```bash
    python3 analysis/download_data.py
    ```
    Expected Outputs:
    - `analysis/data/AAPL.csv`
    - `analysis/data/SPY.csv`
   ---

2. **Market analysis (plots)**
    ```bash
    python3 analysis/part2_analysis.py
    ```
   Expected Outputs:
   - `analysis/output/price_history.png`
   - `analysis/output/volatility.png`

3. **Strategy backtest (20/50 MA crossover)**
    ```bash
    python3 analysis/part3_strategy.py
    ```
   Expected Outputs:
   - `analysis/output/strategy_equity.png` 
   - `analysis/output/metrics_part3.json`

## Run the dashboard (Flask) 🖥️
**Copy precomputed results into the web app**
```bash
cp analysis/output/*.png webapp/static/
cp analysis/output/metrics_part3.json webapp/data/
```

## Start server 🚀
```bash
python3 webapp/app/views.py
```

**Open on Browser:**
- `http://127.0.0.1:5000/` (Dashboard)
- `http://127.0.0.1:5000/data/` (Data preview)
- `http://127.0.0.1:5000/results/` (Plots & metrics)

### **Quick Note**
- Reports on each part of the project is in the `analysis/Deliverables/` folder
- Proof of the web app running is the `webapp/Screenshots/` folder.

### Author
`Kelvin Ihezue`



   

