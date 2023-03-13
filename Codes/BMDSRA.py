import joblib
import xgboost
import xgboost as xgb
import pandas as pd
import numpy as np

from Codes.FeatureExtraction import FeatureExtraction
from Codes.Preprocessing import validation, sampling


class BMDSRA:
    model: xgb.Booster = None
    scaler = None
    sequence_path = None
    sequence = None
    features = []
    feature_names = []

    def __init__(self, model_path, scaler_path):
        self.model = xgb.Booster()
        self.model.load_model(model_path)
        self.scaler = joblib.load(scaler_path)

    def read_file(self, path):
        if not validation(path):
            raise Exception("The sequence file is not in the correct format.")

        seq = sampling(path)
        fe = FeatureExtraction(seq)

        windows_shannon = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 26, 29, 31, 32, 36, 50]
        res_shannon = fe.entropy_based(windows_shannon, method="shannon")
        windows_tsallis = [7, 8, 9, 10, 11, 13, 14, 16, 17, 18, 21, 38, 39, 40, 50]
        res_tsallis = fe.entropy_based(windows_tsallis, method="Tsallis")
        res_furier = fe.fourier_based(method="zcurve")

        windows_furier = [3, 17, 18, 19]
        res_furier = [res_furier[index-1] for index in windows_furier]
        self.features = [res_shannon, res_tsallis, res_furier]
        self.features = sum(self.features, [])

        self.feature_names = []
        for i in windows_shannon:
            self.feature_names.append("ent_shan_{0}".format(i))
        for i in windows_tsallis:
            self.feature_names.append("ent_tsal_{0}".format(i))
        for i in windows_furier:
            self.feature_names.append("fur_{0}".format(i))

    def predict(self, file_path):
        self.read_file(file_path)
        cols = ['ent_shan_50', 'ent_shan_7', 'ent_shan_8', 'ent_shan_9', 'ent_shan_10', 'ent_shan_14', 'ent_tsal_7',
                'fur_17', 'fur_18', 'ent_shan_15', 'ent_shan_6', 'ent_tsal_13', 'ent_shan_31', 'ent_tsal_14',
                'ent_shan_29', 'ent_tsal_8', 'ent_shan_32', 'ent_shan_13', 'ent_tsal_38', 'ent_tsal_11', 'ent_shan_11',
                'ent_tsal_9', 'ent_tsal_39', 'fur_19', 'ent_tsal_17', 'ent_shan_12', 'ent_tsal_50', 'ent_shan_20',
                'ent_tsal_18', 'ent_tsal_10', 'ent_shan_26', 'ent_shan_19', 'ent_tsal_16', 'ent_shan_36', 'ent_shan_16',
                'ent_tsal_40', 'ent_tsal_21', 'fur_3']

        df = pd.DataFrame(np.array(self.features).reshape(1, len(self.features)), columns=self.feature_names)
        df = df[cols]
        df = pd.DataFrame(self.scaler.transform(df), columns=cols)

        d_test = xgb.DMatrix(df)
        res = self.model.predict(d_test)
        labels = ['Amplicon', 'Isolated', 'Metagenome', 'SAGs']
        index = np.argmax(res)
        return labels[index]
