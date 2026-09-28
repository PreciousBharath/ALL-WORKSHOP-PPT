"""Small helper: train / save / load sklearn pipelines with metrics for the dashboard."""
import joblib, numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import (accuracy_score, f1_score, precision_score, recall_score, confusion_matrix,
                             r2_score, mean_absolute_error, mean_squared_error)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def train(df, features, target, task, cats):
    nums = [c for c in features if c not in cats]
    X, y = df[features], df[target]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42,
                                          stratify=y if task == "clf" else None)
    pre = ColumnTransformer([("n", StandardScaler(), nums),
                             ("c", OneHotEncoder(handle_unknown="ignore"), cats)])
    if task == "clf":
        est = RandomForestClassifier(n_estimators=300, min_samples_leaf=2, random_state=42, n_jobs=-1, class_weight="balanced_subsample")
    else:
        est = TransformedTargetRegressor(
            GradientBoostingRegressor(n_estimators=400, learning_rate=0.06, max_depth=4, random_state=42),
            func=np.log, inverse_func=np.exp)
    pipe = Pipeline([("pre", pre), ("m", est)]).fit(Xtr, ytr)
    pred = pipe.predict(Xte)
    core = est if task == "clf" else pipe.named_steps["m"].regressor_
    names = pipe.named_steps["pre"].get_feature_names_out()
    imp = {f: 0.0 for f in features}
    for n, v in zip(names, core.feature_importances_):
        orig = n.split("__", 1)[1]
        for f in sorted(features, key=len, reverse=True):
            if orig == f or orig.startswith(f + "_"):
                imp[f] += float(v); break
    if task == "clf":
        metrics = dict(accuracy=accuracy_score(yte, pred), precision=precision_score(yte, pred),
                       recall=recall_score(yte, pred), f1=f1_score(yte, pred))
        extra = dict(confusion=confusion_matrix(yte, pred).tolist(), balance=y.value_counts().sort_index().tolist())
    else:
        metrics = dict(r2=r2_score(yte, pred), mae=mean_absolute_error(yte, pred),
                       rmse=float(np.sqrt(mean_squared_error(yte, pred))))
        idx = np.random.RandomState(1).choice(len(yte), min(150, len(yte)), replace=False)
        extra = dict(scatter=[[float(yte.iloc[i]), float(pred[i])] for i in idx])
    return dict(pipe=pipe, metrics={k: float(v) for k, v in metrics.items()},
                importance=dict(sorted(imp.items(), key=lambda kv: -kv[1])), extra=extra, rows=len(df))


def load_or_train(path, *args):
    if path.exists():
        return joblib.load(path)
    bundle = train(*args)
    path.parent.mkdir(exist_ok=True)
    joblib.dump(bundle, path)
    return bundle
