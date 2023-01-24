# Feature Extraction
Various feature extraction method have been published in recent years.
These methods generated some representative number for each sequence files.

Feature Extraction Strategy
<ol>
    <li>Fourier Transform</li>
        <ol>
            <li>Binary + Fourier </li>
            <li> Z-curve + Fourier (19 features) </li>
            <li> Real + Fourier </li>
            <li> Integer + Fourier </li>
            <li> EIIP + Fourier </li>
        </ol>
    <li>Entropy Based</li>
    <ol>
        <li>Shannon</li>
        <li>Tsallis</li>
    </ol>
    <li>Graph Based</li>
    <ol>
        <li>CN (with threshold) </li>
        <li>CN (without threshold) </li>
    </ol>
</ol>

The graph-based methods are so time-consuming, particularly when the sequence context is so long.
Because of this, we did not use it.
Fourier-based methods are also time-consuming but not as long as Graph-based methods. Thus we just used the Z-curve Furrier method.
It is worth mentioning that by using the Z-curve Furrier method, we will have 19 representative numbers.
The entropy-based features are so fast and straightforward, so we used both Shannon and Tsallis to apply with different k-mer sizes.
In this study, we extract entropy from 50 different sizes of k-mere. (entropy from k-mer-1, until the entropy from k-mer with the size of 50)
This way is repeated for Tsallis entropy as well.
At the end we will have the 120 various features, (id + 119 representative numbers).