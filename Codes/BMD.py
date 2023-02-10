import getopt
import math
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from xgboost import cv
from Codes.QPFS import QPFS


def main():
    path = "..\\resource\\3-features\\training_data.csv"
    train_data = pd.read_csv(path, header=0, index_col=0)
    indexes = train_data['outliers'] == False
    train_data = train_data[indexes]
    train_data.drop(columns='outliers', inplace=True)
    scale = StandardScaler()
    scaled_data = pd.DataFrame(scale.fit_transform(train_data.drop(columns='label')))
    scaled_data['label'] = train_data['label'].tolist()
    scaled_data['label'] = scaled_data['label'].astype('category')
    scaled_data.columns = train_data.columns
    scaled_data.index = train_data.index

    qp = QPFS(scaled_data.copy())
    importance = qp.get_weight()
    importance.to_csv("..\\resource\\3-features\\importance.csv")
    importance_features_plot()

    # feature_forward_addition(scaled_data, importance)
    # feature_forward_curve_plot()

    # According to the FFA curve, 38 most informative feature should be enough to have an accurate model.
    threshold = 38
    selected_features = importance['name'][0:threshold].tolist()
    selected_columns = selected_features
    selected_columns.append("label")
    print(selected_features)

    scaled_data = scaled_data[selected_columns]
    scaled_data['label'] = scaled_data['label'].cat.codes
    scaled_data_x = scaled_data.iloc[:, :-1]
    scaled_data_y = scaled_data.iloc[:, -1]

    data_dmatrix = xgb.DMatrix(data=scaled_data_x, label=scaled_data_y)
    param = {'eta': 0.25, 'max_depth': 15, 'min_child_weight': 1, 'gamma': 1e-4,
             'objective': 'multi:softprob', 'num_class': 4}
    xgb_cv = cv(dtrain=data_dmatrix, params=param, nfold=5, num_boost_round=1000,
                early_stopping_rounds=500, metrics="merror", as_pandas=True, seed=123)

    scores_df = pd.DataFrame(xgb_cv)
    scores_df.to_csv("..\\resource\\4-model\\cross_validation.csv")

    model = XGBClassifier(**param)
    model.fit(scaled_data_x, scaled_data_y)
    model.save_model("..\\resource\\4-model\\model.json")


def importance_features_plot():

    importance = pd.read_csv("..\\resource\\3-features\\importance.csv", index_col=0)
    path = "..\\resource\\0-images\\importance-features.{0}"
    plt.style.use('ggplot')
    plt.figure(figsize=(20, 10))
    plt.bar(importance.iloc[:, 0], importance.iloc[:, 1])
    plt.xlabel("Features Name", labelpad=20)
    plt.ylabel("Importance")
    plt.title("Feature Importance")
    plt.margins(x=0.01)
    plt.xticks(rotation=90, ha='right', fontsize=7)
    plt.savefig(path.format("pdf"))
    plt.savefig(path.format("svg"))


def feature_forward_addition(data: pd.DataFrame, rank):
    ffe = []  # Feature Forward Error
    for threshold in range(2, len(rank)):
        selected_features = rank['name'][0:threshold].tolist()
        selected_columns = selected_features
        selected_columns.append("label")

        sub_data = data[selected_columns]
        sub_data['label'] = sub_data['label'].cat.codes
        sub_data_x = sub_data.iloc[:, :-1]
        sub_data_y = sub_data.iloc[:, -1]

        data_dmatrix = xgb.DMatrix(data=sub_data_x, label=sub_data_y)
        param = {'eta': 0.25, 'max_depth': 15, 'min_child_weight': 1, 'gamma': 1e-4,
                 'objective': 'multi:softprob', 'num_class': 4, 'nthread': 2}
        xgb_cv = cv(dtrain=data_dmatrix, params=param, nfold=3, num_boost_round=1000,
                    early_stopping_rounds=500, metrics="merror", as_pandas=True, seed=123)
        print("#{0} -------------------------".format(threshold))
        print(xgb_cv.tail(1))
        print('------------------------------')
        ffe.append(xgb_cv.tail(1))

    ffe_data_frame = pd.DataFrame(ffe)
    ffe_data_frame.to_csv("..\\resource\\4-model\\ffa.csv")


def feature_forward_curve_plot():
    path = "..\\resource\\4-model\\ffe.csv"
    df = pd.read_csv(path)
    plt.style.use('ggplot')
    plt.figure(figsize=(15, 5))
    plt.plot(df['nf'], df['test-merror-mean'])
    plt.xlabel("The number of selected features")
    plt.ylabel("error rate")
    plt.title("Feature Forward Addition Curve")
    plt.xticks(range(2, 120, 4))
    path = "..\\resource\\0-images\\ffa-curve.{0}"
    plt.savefig(path.format("pdf"))
    plt.savefig(path.format("svg"))


def main_slurm(arguments):
    print("Hello")
    opts, args = getopt.getopt(arguments, "x:p:i:o:")
    for opt, arg in opts:
        if opt == '-x':
            index = int(arg)
        elif opt == '-p':
            num_parallelism = int(arg)

    print("Index:{0}, Total Parallel={1}".format(index, num_parallelism))
    num_lines = 1296
    step = math.floor(num_lines / num_parallelism)
    start_index = range(1, num_lines, step)[index - 1]
    if index != num_parallelism:
        end_index = start_index + step
    else:
        end_index = num_lines
    print("Start:{0}, End:{1}".format(start_index, end_index))

    path = "training_data.csv"
    train_data = pd.read_csv(path, header=0, index_col=0)
    indexes = train_data['outliers'] == False
    train_data = train_data[indexes]
    train_data.drop(columns='outliers', inplace=True)
    scale = StandardScaler()
    scaled_data = pd.DataFrame(scale.fit_transform(train_data.drop(columns='label')))
    scaled_data['label'] = train_data['label'].tolist()
    scaled_data['label'] = scaled_data['label'].astype('category')
    scaled_data.columns = train_data.columns
    scaled_data.index = train_data.index
    selected_columns = scaled_data.columns
    scaled_data = scaled_data[selected_columns]

    print(scaled_data)
    scaled_data['label'] = scaled_data['label'].cat.codes
    scaled_data_x = scaled_data.iloc[:, :-1]
    scaled_data_y = scaled_data.iloc[:, -1]

    count = 0
    data_dmatrix = xgb.DMatrix(data=scaled_data_x, label=scaled_data_y)
    for etha in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
        for max_depth in [5, 8, 10, 12, 15, 20]:
            for min_child_weight in [1, 3, 5, 7, 9, 11]:
                for gamma in [0, 1e-4, 1e-3, 1e-2, 1e-1, 1.0]:
                    count += 1
                    if start_index <= count < end_index:
                        param = {'max_depth': max_depth, 'eta': etha, 'min_child_weight': min_child_weight,
                                 'gamma': gamma,
                                 'objective': 'multi:softprob', 'num_class': 4}
                        xgb_cv = cv(dtrain=data_dmatrix, params=param, nfold=5, num_boost_round=1000,
                                    early_stopping_rounds=500, metrics="merror", as_pandas=True, seed=123)
                        print([etha, max_depth, min_child_weight, gamma] + xgb_cv.tail(1).values.tolist())

    # Best parameters
    # etha	max_depth	min_child_weight	gamma	train-error-mean	train-error-std	test-error-mean	test-error-std
    # 0.25	15	        1	                0.0001	0.0018932	        0.000272628	    0.0727838	    0.004406073


if __name__ == '__main__':
    # feature_forward_curve_plot()
    # main_slurm(sys.argv[1:])
    # importance_features_plot()
      main()
