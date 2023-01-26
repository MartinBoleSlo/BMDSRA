import math
import statistics
import numpy as np
from scipy.fftpack import fft, ifft


class FeatureExtraction:
    seq = ''
    information_entropy = []
    spectrum = []
    spectrumTwo = []
    spectrum_features = []

    def __init__(self, seq):
        self.seq = seq.upper()
        print('')

    def entropy_based(self, windows, method="shannon"):
        self.information_entropy = []
        for win in windows:
            probabilities = []
            kmer = {}
            total_windows = (len(self.seq) - win) + 1  # (L - k + 1)
            for subseq in self.chunks(win):
                if subseq in kmer:
                    kmer[subseq] = kmer[subseq] + 1
                else:
                    kmer[subseq] = 1
            for key, value in kmer.items():
                probabilities.append(value / total_windows)
            if method.lower() == "shannon":
                entropy_equation = [(p * math.log(p, 2)) for p in probabilities]
                entropy = -(sum(entropy_equation))
                self.information_entropy.append(entropy)
            else:
                q = 2
                entropy_equation = [(p ** q) for p in probabilities]
                entropy = (1 / (q - 1)) * (1 - sum(entropy_equation))
                self.information_entropy.append(entropy)
        return self.information_entropy

    def chunks(self, win):
        seq_len = len(self.seq)
        for i in range(seq_len):
            j = seq_len if i + win > seq_len else i + win
            yield self.seq[i:j]
            if j == seq_len:
                break
        return

    def fourier_based(self, method="zcurve"):
        self.spectrum = []
        self.spectrumTwo = []
        self.spectrum_features = []
        self.zcurve_fourier()
        self.spectrum_feature_extraction()
        return self.spectrum_features

    def zcurve_fourier(self):
        R = 0  # x[n] = (An + Gn) − (Cn + Tn) ≡ Rn − Yn
        Y = 0
        M = 0  # y[n] = (An + Cn) − (Gn + Tn) ≡ Mn − Kn
        K = 0
        W = 0  # z[n] = (An + Tn) − (Cn + Gn) ≡ Wn − Sn
        S = 0

        x = []
        y = []
        z = []
        for nucle in self.seq:
            if nucle == "A" or nucle == "G":
                R += 1
                x.append((R) - (Y))
            else:
                Y += 1
                x.append((R) - (Y))
            if nucle == "A" or nucle == "C":
                M += 1
                y.append((M) - (K))
            else:
                K += 1
                y.append((M) - (K))
            if nucle == "A" or nucle == "T" or nucle == "U":
                W += 1
                z.append((W) - (S))
            else:
                S += 1
                z.append((W) - (S))
        FX = fft(x)
        FY = fft(y)
        FZ = fft(z)
        for i in range(len(self.seq)):
            specTotal = (abs(FX[i]) ** 2) + (abs(FY[i]) ** 2) + (abs(FZ[i]) ** 2)
            specTwo = (abs(FX[i])) + (abs(FY[i])) + (abs(FZ[i]))
            self.spectrum.append(specTotal)
            self.spectrumTwo.append(specTwo)

    def spectrum_feature_extraction(self):
        self.spectrum_features = []
        average = sum(self.spectrum) / len(self.spectrum)
        self.spectrum_features.append(average)
        median = np.median(self.spectrum)
        self.spectrum_features.append(median)
        maximum = np.max(self.spectrum)
        self.spectrum_features.append(maximum)
        minimum = np.min(self.spectrum)
        self.spectrum_features.append(minimum)
        peak = (len(self.spectrum) / 3) / average
        self.spectrum_features.append(peak)
        peak_two = (len(self.spectrumTwo) / 3) / (np.mean(self.spectrumTwo))
        self.spectrum_features.append(peak_two)
        standard_deviation = np.std(self.spectrum)  # standard deviation
        self.spectrum_features.append(standard_deviation)
        standard_deviation_pop = statistics.stdev(self.spectrum)  # population sample standard deviation
        self.spectrum_features.append(standard_deviation_pop)
        percentile15 = np.percentile(self.spectrum, 15)
        self.spectrum_features.append(percentile15)
        percentile25 = np.percentile(self.spectrum, 25)
        self.spectrum_features.append(percentile25)
        percentile50 = np.percentile(self.spectrum, 50)
        self.spectrum_features.append(percentile50)
        percentile75 = np.percentile(self.spectrum, 75)
        self.spectrum_features.append(percentile75)
        amplitude = maximum - minimum
        self.spectrum_features.append(amplitude)
        variance = statistics.variance(self.spectrum)
        self.spectrum_features.append(variance)
        inter_quartile_range = np.percentile(self.spectrum, 75) - np.percentile(self.spectrum, 25)
        self.spectrum_features.append(inter_quartile_range)
        semi_inter_quartile_range = (np.percentile(self.spectrum, 75) - np.percentile(self.spectrum, 25)) / 2
        self.spectrum_features.append(semi_inter_quartile_range)
        coefficient_of_variation = standard_deviation / average
        self.spectrum_features.append(coefficient_of_variation)
        skewness = (3 * (average - median)) / standard_deviation
        self.spectrum_features.append(skewness)
        kurtosis = (np.percentile(self.spectrum, 75) - np.percentile(self.spectrum, 25)) / (
                2 * (np.percentile(self.spectrum, 90) - np.percentile(self.spectrum, 10)))
        self.spectrum_features.append(kurtosis)
