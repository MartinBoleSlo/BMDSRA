# BMD-SRA: A Boosting Model for Differentiating Sequence Read Archive Files Based on the Context. 

The volume of the deposit sequence file is increase dramatically.
Also, the submitter of the sequence file is main responsible for annotating.
Although the submitter and public repositories pay attention to making accurate metadata, mistakes can happen.
These issues can cause troubles in performing downstream analysis.
BMD-SRA tries to differentiate the given sequence files into four categories including
<ol>
    <li>Meta Genomes</li>
    <li>Amplicons</li>
    <li>Single Amplified Genomes (SAGs) </li>
    <li>Isolated Genomes</li>
</ol>

For developing this model, some stages were tracked, which listed below:
<ol>
    <li>Preparing Metadata</li>
    <li>Downloading Sequence Files</li>
    <li>Feature Extraction</li>
    <li>Outlier Detection</li>
    <li>Developing Model</li>
    <li>Evaluation Model</li>
</ol>