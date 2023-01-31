## Feature Evaluation

As mentioned before, the 120 features are extracted from sequence files.
The major question is which features are most informative and which those are irrelative.
To answering this question, all extracted features are evaluated by applying the multi-variate method called QPFS.
The result of the evaluation is illustrated in the below image.
It shows that the most informative features are Entropy-Shannon with k-mers sizes 7, 8, and 9.
Although the most of them can be removed to have simpler model.

![Importance of features](../resource/images/importance.svg)
