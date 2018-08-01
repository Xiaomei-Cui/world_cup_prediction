# This file contains machine learning code.
# Modified from GCForest example machine learning code
"""
Usage:
    define the model within scripts:
        python examples/demo_mnist.py
    get config from json file:
        python examples/demo_mnist.py --model examples/demo_mnist-gc.json
        python examples/demo_mnist.py --model examples/demo_mnist-ca.json
"""
import argparse
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
# sys.path.insert(0, "..\\lib")

from lib.gcforest.gcforest import GCForest
from lib.gcforest.utils.config_utils import load_json


# parse args if config is read from files
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", dest="model", type=str, default=None, help="gcfoest Net Model File")
    args = parser.parse_args()
    return args


# set configulations
def set_config():
    config = {}
    ca_config = {}
    ca_config["random_state"] = 0
    ca_config["max_layers"] = 200  # 12
    ca_config["early_stopping_rounds"] = 30  # stop early if no improvement
    ca_config["n_classes"] = 10
    ca_config["estimators"] = []

    default_folds = 1  # 5
    default_estimators = 10  # 10
    ca_config["estimators"].append(
        {"n_folds": default_folds, "type": "XGBClassifier", "n_estimators": default_estimators, "max_depth": 10000,  # 5
         "objective": "multi:softprob", "silent": True, "nthread": -1, "learning_rate": 0.3})
    ca_config["estimators"].append(
        {"n_folds": default_folds, "type": "RandomForestClassifier", "n_estimators": default_estimators,
         "max_depth": None, "n_jobs": -1})
    ca_config["estimators"].append(
        {"n_folds": default_folds, "type": "ExtraTreesClassifier", "n_estimators": default_estimators,
         "max_depth": None, "n_jobs": -1})
    ca_config["estimators"].append(
        {"n_folds": default_folds, "type": "LogisticRegression"})
    config["cascade"] = ca_config
    return config


# main
if __name__ == "__main__":

    args = parse_args()
    if args.model is None:
        config = set_config()
    else:
        # using --model xxxx.json
        config = load_json(args.model)

    X_train = np.load("X_train.npy")
    X_test = np.load("X_test.npy")
    y_train = np.load("y_train.npy")
    y_test = np.load("y_test.npy")
    config["cascade"]["n_classes"] = len(np.unique(y_train))

    gc = GCForest(config)
    # If the model you use cost too much memory for you.
    # You can use these methods to force gcforest not keeping model in memory
    # gc.set_keep_model_in_mem(False), default is TRUE.

    # training:
    X_train_enc = gc.fit_transform(X_train, y_train)

    # X_enc is the concatenated predict_proba result
    # of each estimators of the last layer of the GCForest model
    # X_enc.shape =
    #   (n_datas, n_estimators * n_classes): If cascade is provided
    #   (n_datas, n_estimators * n_classes, dimX, dimY): If only finegrained part is provided
    # You can also pass X_test, y_test to fit_transform method,
    # then the accracy on test data will be logged when training.
    #   X_train_enc, X_test_enc = gc.fit_transform(X_train, y_train, X_test=X_test, y_test=y_test)
    # WARNING: if you set gc.set_keep_model_in_mem(True), you would have to use
    # gc.fit_transform(X_train, y_train, X_test=X_test, y_test=y_test) to evaluate your model.

    y_pred = gc.predict(X_test)
    print("y_pred: %s" % y_pred)

    # You can try passing X_enc to another classfier on top of gcForest.e.g. xgboost/RF.
    X_test_enc = gc.transform(X_test)
    X_train_enc = X_train_enc.reshape((X_train_enc.shape[0], -1))
    X_test_enc = X_test_enc.reshape((X_test_enc.shape[0], -1))
    X_train_origin = X_train.reshape((X_train.shape[0], -1))
    X_test_origin = X_test.reshape((X_test.shape[0], -1))
    X_train_enc = np.hstack((X_train_origin, X_train_enc))
    X_test_enc = np.hstack((X_test_origin, X_test_enc))
    # print("X_train_enc.shape={}, X_test_enc.shape={}".format(X_train_enc.shape, X_test_enc.shape))

    clf = RandomForestClassifier(n_estimators=1000, max_depth=None, n_jobs=-1)
    clf.fit(X_train_enc, y_train)
    y_pred = clf.predict(X_test_enc)
    print("y_pred: %s" % y_pred)

    # dump
    with open("test.pkl", "wb") as f:
        pickle.dump(gc, f, pickle.HIGHEST_PROTOCOL)
    # load
    with open("test.pkl", "rb") as f:
        gc = pickle.load(f)
    y_pred = gc.predict(X_test)
    print("y_pred: %s" % y_pred)
