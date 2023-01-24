
# Downloading Sequence Files, Sudolf

For developing a model, it is necessary to download the sequence files.
To this matter, the [Fastq-dump](https://rnnh.github.io/bioinfo-notebook/docs/fastq-dump.html) is used.
It is worth mentioning that downloading and processing the 12000 sequence files are voluminous and time-consuming.
Indeed, for making an AI model, processing the whole context of sequence files is unnecessary, thus in this study, just 3000 of various reads in the sequence files are downloaded and processed.
For downloading the small portion of the given sequence file identification (Run Accession Number), the new version of the traditional fastq-dump third-party tool is developed.
This tool called SuDolF (**Su**bsampling and **Do**wn**l**oading **F**astq Files).
The SuDolF tool tries to download various spots from different places of a sequence file in the multi-independent threads.
So

