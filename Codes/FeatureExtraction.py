import math


class FeatureExtraction:
    seq = ''
    information_entropy = []

    def __init__(self, seq):
        self.seq = seq.upper()
        print('')

    def entropy_based(self, windows, method="shanon"):
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

    def fourier_based(self):
        print('')
