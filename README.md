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

# How can you use it?
There are two ways for using the outcomes of the study. Generating your own model or Applying the generated model in your project.
## Generating your own model
There is well-form documentation about preparing [training data](resource/3-features/features.csv) 
You can use the extracted features and generate your own model.

## Load the generated model and apply it.
The generated model is accessible here.
You can use the BMDSRA class and pass just two parameters to make an object.

<ol>
    <li> The path of the model.</li>
    <li> The path of the scaler.</li>
</ol>
After making an object of the BMDSRA class, just call predict function and pass the path of the sequence file.

It is worth mentioning that the BMD-SRA needs access to two files, including [FeatureExtraction](Codes/FeatureExtraction.py) and [Preprocessing](Codes/Preprocessing.py).
Also, accessing to the xgboost package is essential.

## Example:
    from Codes.BMDSRA import BMDSRA
    model_path = "..\\..\\resource\\4-model\\model.json"
    scaler_path = "..\\..\\resource\\4-model\\scaler.gz" 
    model = BMDSRA(model_path, scaler_path)

    seq_path = "..\\..\\resource\\2-subsra\\SRR1588386.fastq" 
    res = model.predict(seq_path)
    print(res)

To reach more sample about the running model you can see [here](Codes/test/BMDSRA.py)