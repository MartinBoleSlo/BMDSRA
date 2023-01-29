import numpy as np
import pandas
import pandas as pd
from sklearn.metrics import mutual_info_score
from qpsolvers import solve_qp
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from numpy import linalg as la


class QPFS:
    data = None
    su = None
    features = None
    target = None
    uncertainty_matrix: np.matrix = []

    def __init__(self, data: pandas.DataFrame = pandas.DataFrame(), target="label"):
        self.target = target
        if not data.empty:
            self.data = data
            self.target = target
            self.data[target] = self.data[target].astype('category')
            self.data[target] = self.data[target].cat.codes

    def symmetric_uncertainty(self):

        self.discretize(20)
        nc = self.data.shape[1]
        ff_MI = np.zeros((nc, nc))
        ff_SU = np.zeros((nc, nc))
        for i in range(0, nc):
            for j in range(0, nc):
                v = 0
                if i <= j:
                    v = mutual_info_score(self.data.iloc[:, i], self.data.iloc[:, j])
                else:
                    v = ff_MI[j, i]
                ff_MI[i, j] = v

        for i in range(0, nc):
            for j in range(0, nc):
                if i == j:
                    ff_SU[i, j] = 1
                elif i < j:
                    ff_SU[i, j] = 2 * ff_MI[i, j] / (ff_MI[i, i] + ff_MI[j, j])
                    ff_SU[j, i] = ff_SU[i, j]

        self.uncertainty_matrix = ff_SU

    def discretize(self, bins):
        for col in self.data.columns:
            split = np.array_split(np.sort(self.data[col]), bins)
            cutoffs = [x[-1] for x in split]
            cutoffs = cutoffs[:-1]
            discrete = np.digitize(self.data[col], cutoffs, right=True)
            self.data[col] = discrete

    def get_weight(self, a: float = 0.0):
        self.symmetric_uncertainty()
        nc = self.uncertainty_matrix.shape[0]
        nf = nc - 1
        ff: np.matrix = self.uncertainty_matrix[0:nf, 0:nf]
        fc: np.array = self.uncertainty_matrix[nf, 0:nf]
        weights = self.solve_QP(ff, fc)
        columns = self.data.columns[0:nf]
        importance = pd.DataFrame([columns, weights.tolist()]).T
        importance.columns = ['name', 'weight']
        importance.sort_values(ascending=False, inplace=True, by='weight')
        return importance

    def solve_QP(self, H: np.matrix, f: np.array, a: float = 0.0):

        if not self.isPD(H):
            H = self.nearestPD(H)

        nf = H.shape[0]
        mean_H = H.mean()
        mean_f = f.mean()
        alpha = a
        if alpha == 0.0:
            alpha = mean_H / (mean_H + mean_f)

        if alpha < 0 or alpha > 1:
            raise Exception("The alpha factor is not valid.")

        P = H * (1 - alpha)
        q = -1 * f * alpha

        # Equalities => sum of all weight should be equal one
        # Ax = b
        # [1, 1, 1] = [1]

        A = np.ones([nf])
        b = np.ones([1])

        # Inequality => all of the features should be bigger than zero
        # Gx <= h
        # -1, 0 , 0
        # 0 ,-1 , 0
        # 0 , 0 , -1
        h = np.zeros([nf])
        G: np.matrix = np.zeros([nf, nf])
        for i in range(0, nf):
            for j in range(0, nf):
                if i == j:
                    G[i, j] = -1

        weights = solve_qp(P, q, G, h, A, b, solver='quadprog')
        return weights

    def nearestPD(self, matrix: np.matrix):
        """Find the nearest positive-definite matrix to input

        A Python/Numpy port of John D'Errico's `nearestSPD` MATLAB code [1], which
        credits [2].

        [1] https://www.mathworks.com/matlabcentral/fileexchange/42885-nearestspd

        [2] N.J. Higham, "Computing a nearest symmetric positive semidefinite
        matrix" (1988): https://doi.org/10.1016/0024-3795(88)90223-6
        """

        B = (matrix + matrix.T) / 2
        _, s, V = la.svd(B)

        H = np.dot(V.T, np.dot(np.diag(s), V))

        A2 = (B + H) / 2

        A3 = (A2 + A2.T) / 2

        if self.isPD(A3):
            return A3

        spacing = np.spacing(la.norm(matrix))
        # The above is different from [1]. It appears that MATLAB's `chol` Cholesky
        # decomposition will accept matrixes with exactly 0-eigenvalue, whereas
        # Numpy's will not. So where [1] uses `eps(mineig)` (where `eps` is Matlab
        # for `np.spacing`), we use the above definition. CAVEAT: our `spacing`
        # will be much larger than [1]'s `eps(mineig)`, since `mineig` is usually on
        # the order of 1e-16, and `eps(1e-16)` is on the order of 1e-34, whereas
        # `spacing` will, for Gaussian random matrixes of small dimension, be on
        # othe order of 1e-16. In practice, both ways converge, as the unit test
        # below suggests.
        I = np.eye(matrix.shape[0])
        k = 1
        while not self.isPD(A3):
            mineig = np.min(np.real(la.eigvals(A3)))
            A3 += I * (-mineig * k ** 2 + spacing)
            k += 1

        return A3

    def isPD(self, matrix: np.matrix):
        """Returns true when input is positive-definite, via Cholesky"""
        try:
            _ = la.cholesky(matrix)
            return True
        except la.LinAlgError:
            return False


def __del__(self):
    print('')
