import numpy as np
import pandas
import pandas as pd
from sklearn.metrics import mutual_info_score
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.preprocessing import KBinsDiscretizer

class QPFS:
    data = None
    su = None
    features = None
    target = None

    def __init__(self, data: pandas.DataFrame, target: int):
        self.data = data
        self.target = target



    def symmetric_uncertainty(self):

        nc = self.data.shape[1]
        label = self.data[['label']]
        features = self.data.drop(columns='label')
        ff_MI = pandas.DataFrame(data=None, columns=range(1, nc))
        for f in features:
            mir = mutual_info_regression(features, features[f])
            ff_MI.loc[len(ff_MI), :] = mir

        fc_MI = mutual_info_classif(features, label)

        ff_SU = pandas.DataFrame(data=None, columns=range(1, nc))
        for i in ff_SU:
            for j in ff_SU:
                if i == j:
                    ff_SU[i, j] = 1
                elif i < j:
                    ff_SU[i, j] = 2 * ff_MI[i, j] / (ff_MI[i, i] + ff_MI[j, j])
                    ff_SU[j, i] = ff_SU[i, j]

        fc_SU = [0] * len(fc_MI)
        for i in fc_SU:
            fc_SU[i] = 2 * fc_MI / (ff_MI[i,i] + fc_MI[i,i])


        print(fc_MI)
        #+ [mutual_info_classif(features[f], label)]

    def __del__(self):
        print('')
