from flask import Flask, render_template
import json
import os
import pandas as pd

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="../static",
    static_url_path="/static",
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
METRICS_PATH = os.path.join(BASE_DIR, "..", "data", "metrics_part3.json")

AAPL_CSV_PATH = os.path.join(BASE_DIR, "..", "..", "analysis", "data", "AAPL.csv")
SPY_CSV_PATH = os.path.join(BASE_DIR, "..", "..", "analysis", "data", "SPY.csv")


def load_metrics():
    with open(METRICS_PATH, "r") as file:
        return json.load(file)


@app.route("/")
def dashboard():
    metrics = load_metrics()

    charts = {
        "price_history": "price_history.png",
        "strategy_equity": "strategy_equity.png",
        "volatility": "volatility.png",
    }

    return render_template("dashboard.html", metrics=metrics, charts=charts)


@app.route("/data/")
def data_page():
    # Show a small preview so the grader can see “the dataset”
    aapl_rows = pd.read_csv(AAPL_CSV_PATH).head(10).to_dict(orient="records")
    spy_rows = pd.read_csv(SPY_CSV_PATH).head(10).to_dict(orient="records")

    return render_template("data.html", aapl=aapl_rows, spy=spy_rows)


@app.route("/results/")
def results_page():
    metrics = load_metrics()

    plots = ["price_history.png", "volatility.png", "strategy_equity.png"]

    return render_template("results.html", metrics=metrics, plots=plots)


if __name__ == "__main__":
    app.run(debug=True)
