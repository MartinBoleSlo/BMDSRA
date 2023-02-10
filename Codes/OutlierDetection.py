import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib as mpl
import matplotlib.pyplot as plt
from Codes.QPFS import QPFS


def main():
    path = "..\\resource\\3-features\\features.csv"
    data = pd.read_csv(path, header=0, index_col=0)

    scale = StandardScaler()
    scaled_data = pd.DataFrame(scale.fit_transform(data.drop(columns='label')))
    scaled_data['label'] = data['label'].tolist()
    scaled_data['label'] = scaled_data['label'].astype('category')
    scaled_data.columns = data.columns
    scaled_data.index = data.index

    qp = QPFS(scaled_data.copy())
    importance = qp.get_weight()
    selected_features = importance['name'][0:2].tolist()

    selected_features.append('label')
    sub_data = scaled_data[selected_features]
    outlier_indexes = []
    outlier_indexes.extend(outlier_plot(sub_data, 'SAGs'))
    outlier_indexes.extend(outlier_plot(sub_data, 'Isolated'))
    outlier_indexes.extend(outlier_plot(sub_data, 'Metagenome'))
    outlier_indexes.extend(outlier_plot(sub_data, 'Amplicon'))

    data['outliers'] = False
    data.loc[outlier_indexes, 'outliers'] = True
    path = "..\\resource\\3-features\\training_data.csv"
    data.to_csv(path)


def outlier_plot(data, label):
    eps = 0.3
    minPts = len(data.columns)
    indexes = data['label'] == label
    sub_scaled_data = data[indexes].copy()
    sub_scaled_data.drop(columns='label', inplace=True)
    clustering = DBSCAN(eps=eps, min_samples=minPts).fit(sub_scaled_data)
    clusters = clustering.labels_
    mf = most_frequent(clusters.tolist())
    indexes = clusters == mf
    clusters[indexes] = False
    clusters[~indexes] = True
    sub_scaled_data['clusters'] = clusters
    sub_scaled_data['clusters'] = sub_scaled_data['clusters'].astype('category')

    plt.style.use('ggplot')
    sub_scaled_data.plot(kind='scatter', x=sub_scaled_data.columns[0], y=sub_scaled_data.columns[1], c='clusters',
                         cmap=mpl.colormaps['viridis'])
    plt.title("{0} Outliers".format(label))
    path = "..\\resource\\0-images\\{0}_outlier.{1}"
    plt.savefig(path.format(label, "pdf"))
    plt.savefig(path.format(label, "svg"))
    return sub_scaled_data.index[sub_scaled_data['clusters'] == 1].tolist()


def most_frequent(lst):
    return max(set(lst), key=lst.count)


if __name__ == '__main__':
    main()
