import config

from flask import Flask, request, jsonify, abort
from flask.app import HTTPException
from sqlalchemy import Column, Integer, String, JSON, Boolean
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import Ridge
import numpy as np
import pandas as pd

def training(data, target, n_folds, intercept, l2_coef):
    all_data = [x.split(',') for x in data.split('\n')]
    columns = all_data[0]
    data = all_data[1:]
    df = pd.DataFrame(data, columns=columns)
    y = df[target]
    X = df.drop(target, axis=1)

    for l2 in l2_coef:
        model = Ridge(alpha=l2, fit_intercept=intercept)
        model.fit(X, y)
        kf = KFold(n_splits=n_folds)
        results = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')
    return results


Base = declarative_base()
engine = create_engine(
    config.server_url
)
## postgres - username
## mysecretpassword - password
### потом вынести в config

def init_db():
    Base.metadata.create_all(engine)

class Model(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True, autoincrement=True)
    results = Column(JSONB)

init_db()

app = Flask(__name__)
session_factory = sessionmaker()

@app.errorhandler(Exception)
def error_handler(exc):
    if isinstance(exc, HTTPException):
        return jsonify({"error": exc.description}), exc.code
    print(exc)
    return jsonify({"error": "internal error"}), 500

@app.route('/train', methods=['POST'])
def train_a_net():
    data_json = request.get_json()
    try:
        data = str(data_json['data'])
        target = str(data_json['target'])
        n_folds = int(data_json['n_folds'])
        fit_intercept = bool(data_json['fit_intercept'])
        l2_coef = list(data_json['l2_coef'])
    except Exception as exc:
        abort(400, f"invalid data: {exc}")
        return
    training(data, target, n_folds, fit_intercept, l2_coef)
    session = session_factory()
    model = Model(data=data, target=target, n_folds=n_folds, fit_intercept=fit_intercept, l2_coef=l2_coef, ready=True)
    session.add(model)
    session.commit()
    return jsonify({"model_id": model.id})

@app.route('/model/<int:model_id>', methods=['GET'])
def get_model(model_id):
    session = session_factory()
    model = session.query(Model).filter_by(id=model_id).first()
    if model is None:
        abort(404, f"model {model_id} not found")
        return
    
    return jsonify({
        "results": results,
    })

##@app.route('/model/<int:model_id>/predict', methods=['POST'])

app.run()

