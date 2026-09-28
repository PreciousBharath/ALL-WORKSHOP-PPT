"""Flask app. Run:  python app.py   (models train automatically on first run)."""
import os
from pathlib import Path
import numpy as np, pandas as pd
from flask import Flask, abort, jsonify, render_template, request, send_from_directory
import make_data, mlkit
from specs import PROJECT, SPECS

BASE = Path(__file__).parent
DATA, MODELS = BASE / "data", BASE / "models"
app = Flask(__name__)

make_data.build_all(DATA)
BUNDLES = {}
for key, s in SPECS.items():
    df = pd.read_csv(DATA / s["csv"])
    feats = [f["name"] for f in s["fields"]]
    cats = [f["name"] for f in s["fields"] if f["type"] == "select"]
    BUNDLES[key] = mlkit.load_or_train(MODELS / f"{key}.joblib", df, feats, s["target"], s["task"], cats)


def spec_or_404(key):
    if key not in SPECS: abort(404)
    return SPECS[key], BUNDLES[key]


def make_row(s, vals):
    row = {}
    for f in s["fields"]:
        v = vals.get(f["name"], f.get("default"))
        if f["type"] == "select":
            v = str(v)
            if v not in f["options"]: raise ValueError(f"Invalid {f['label']}")
            row[f["name"]] = v
        else:
            row[f["name"]] = float(np.clip(float(v), f["min"], f["max"]))
    return pd.DataFrame([row])


def score(s, b, df):
    if s["task"] == "clf":
        p = b["pipe"].predict_proba(df)
        return p[:, list(b["pipe"].classes_).index(1)]
    return b["pipe"].predict(df)


@app.route("/")
def home():
    cards = []
    for k, s in SPECS.items():
        m = BUNDLES[k]["metrics"]
        head = ("Accuracy", m["accuracy"] * 100, "%") if s["task"] == "clf" else ("R² score", m["r2"] * 100, "%")
        cards.append(dict(key=k, title=s["title"], icon=s["icon"], tagline=s["tagline"], metric=head,
                          rows=BUNDLES[k]["rows"], task=s["task"], nf=len(s["fields"])))
    return render_template("index.html", P=PROJECT, cards=cards)


@app.route("/model/<key>")
def model_page(key):
    s, b = spec_or_404(key)
    pub = {k: v for k, v in s.items() if k != "csv"}
    return render_template("model.html", P=PROJECT, s=pub, metrics=b["metrics"], key=key)


@app.post("/api/predict/<key>")
def predict(key):
    s, b = spec_or_404(key)
    try:
        df = make_row(s, request.get_json(force=True))
    except (ValueError, TypeError) as e:
        return jsonify(error=str(e)), 400
    v = float(score(s, b, df)[0])
    if s["task"] == "clf":
        lvl = s["levels"][0 if v < .25 else 1 if v < .5 else 2 if v < .75 else 3]
        return jsonify(prob=v, label=s["labels"][int(v >= .5)], level=lvl, tips=s["tips"][str(int(v >= .5))])
    mae = b["metrics"]["mae"]
    out = dict(value=v, low=max(v - mae, 0.1), high=v + mae)
    if "area_sqft" in df: out["per_sqft"] = v * 1e5 / float(df["area_sqft"][0])
    return jsonify(out)


@app.post("/api/whatif/<key>")
def whatif(key):
    s, b = spec_or_404(key)
    df = make_row(s, request.get_json(force=True))
    f = next(f for f in s["fields"] if f["name"] == s["sweep"])
    xs = np.linspace(f["min"], f["max"], 14)
    grid = pd.concat([df] * len(xs), ignore_index=True)
    grid[f["name"]] = xs
    return jsonify(label=f["label"], x=[round(float(x), 2) for x in xs], y=[float(v) for v in score(s, b, grid)])


@app.get("/api/insights/<key>")
def insights(key):
    s, b = spec_or_404(key)
    labels = {f["name"]: f["label"] for f in s["fields"]}
    return jsonify(metrics=b["metrics"], rows=b["rows"], task=s["task"], classes=s.get("labels"),
                   importance=[[labels[k], v] for k, v in b["importance"].items()], **b["extra"])


@app.get("/download/<key>")
def download(key):
    s, _ = spec_or_404(key)
    return send_from_directory(DATA, s["csv"], as_attachment=True)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", PROJECT["port"])), debug=False)
