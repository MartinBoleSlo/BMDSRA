# BMD-SRA: A Boosting Model for Differentiating Sequence Read Archive Files Based on the Context. 

The volume of the sequences files deposited in the Sequence Read Archive (SRA) has increased dramatically over the years.
The responsibility of submission of correctly annotated sequences mainly falls on the submitter of such data.
Although the main goal of submitters and public repositories should be to make metadata conform to FAIR principles, mistakes can happen.
These issues of mislabeled data can then cause problems in performing downstream analysis of samples.
BMD-SRA tries to avoid such mistakes by differentiating the input given (prokaryote sequences in fastq format) into four categories:
<ol>
    <li>Metagenomes</li>
    <li>Amplicons</li>
    <li>Single Amplified Genomes (SAGs) </li>
    <li>Isolated Genomes</li>
</ol>

When developin this model, we followed the stages listed bellow:
<ol>
    <li>Preparing Metadata</li>
    <li>Downloading Sequence Files From SRA</li>
    <li>Feature Extraction</li>
    <li>Outlier Detection</li>
    <li>Development Of The Model</li>
    <li>Evaluation Of The Model</li>
</ol>

# How can you use it?
There are two ways for using the outcome of this project. 
  * Generating your own model with the code provided
  OR
  * Applying the generated model from this project to your own study.
## Generating your own model
When generating your own model you first need to prepare [training data](resource/3-features/features.csv) 
You can use the extracted features to then generate your own model.

## Applying the generated model from this project to your own study.
The generated model is accessible here.
You can use the BMDSRA class and pass just two parameters.
<ol>
    <li> The path of the model.</li>
    <li> The path of the sequence file (fastq) </li>
</ol>

It is worth mentioning that the BMD-SRA needs access to two files, including [FeatureExtraction](Codes/FeatureExtraction.py) and [Preprocessing](Codes/Preprocessing.py).

## Example:
    #Import the BMDSRA module
    from Codes.BMDSRA import BMDSRA
    # Set the path of the model either your own model or generated model (from this study)
    model_path = "..\\..\\resource\\4-model\\model.json"
    # Set the path of the sequence file (fastq)
    seq_path = "..\\..\\resource\\2-subsra\\SRR1588386.fastq"
    # Apply model path to the imported BMDSRA module
    model = BMDSRA(model_path)
    # Calling predict function on provided sequence file (fastq) path
    res = model.predict(seq_path)
    # View the results
    print(res)
