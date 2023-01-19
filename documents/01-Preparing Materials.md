

# Preparing Materials.

---
The expectation is that the produced model can differentiate the various sequence files.
Thus, the target labels are including: 
<ol>
<li>Meta Genomes </li>
<li>Amplicons</li>
<li>Single Amplified Genomes (SAGs)</li>
<li>Isolated Genomes</li>
</ol>

## Material of Meta-Genome
for preparing the MetaGenome material, the four datasets which are published formerly has been used.
<ol>
<li> MarineMetagenomeDB [Link](https://webapp.ufz.de/marmdb/) </li>
<li> HumanMetagenomeDB (https://webapp.ufz.de/hmgdb/) </li>
<li> AnimalAssociatedMetagenomeDB (https://webapp.ufz.de/aamdb/) </li>
<li> TerrestrialMetagenomeDB (https://webapp.ufz.de/tmdb/) </li>
</ol>

The records containing less than 20M reads were filtered.
Among each environment, 750 different samples were selected randomly.
In the end, 3000 various MetaGenome samples from different environments were selected [Link]().

## Material of Amplicon
For preparing the material of Amplicon sequence, the corresponding metadata is fetched from [JGI](https://genome.jgi.doe.gov/portal/) portal.
In the JGI portal, the projects whose 'strategy library' are set to 'AMPLICON', were extracted.
Then, 3000 records as diverse as possible were selected.
The below list illustrates that the selected records belong to which sub-categories.
<ol>
<li>Environment</li>
    <ul>
    <li>Soil: 1216 | Marine: 574 | Water: 116 | Human: 322 </li>
    </ul>
<li>Primer</li>
    <ul>
    <li>16s: 742 | 18s: 484 | ITS: 291 </li>
    </ul>
<li>Region</li>
    <ul>
    <li>V1: 94 | V2: 11 | V3: 76 | V4: 63 | V5: 12 | V6: 12 </li>
    </ul>
</ol>

## Material of Single Amplified Genomes (SAGs)

Finding the metadata of samples belonging to SAGs category is not strait forward.
To this matter, some metadata of the NCBI SRA were extracted such that their corresponding published paper contains explicit expressions about the study and the type of the sequence files.
In the end, as same as other investigated sequence types, 3000 records were selected.

## Material of Isolated Genome

For preparing the Isolated Genome, the corresponding the metadata the NCBI portal were searched by using the term of 'Bacteria type strain Genome'.
Moreover, to get as diverse as possible, the hierarchy taxonomy were determined bz using Gtdbk.
In the end, 3000 records were selected such a way no two records belonged to the same species.
The below list illustrates that distribution taxonomy of the selected records.

| Phylum         | Class                                                                                                | n    |
|----------------|------------------------------------------------------------------------------------------------------|------|
| Chlamydiae     | Chlamydiae (1)                                                                                       | 1    |
| Cyanobacteria  | Cyanophyceae (1)                                                                                     | 1    |
| Bacteroidetes  | Bacteroidia (1), Cytophagia (1)                                                                      | 2    |
| Actinobacteria | NA                                                                                                   | 45   |
| Firmicutes     | Clostridia (1), Bacilli (52)                                                                         | 54   |
| Proteobacteria | Betaproteobacteria (4), Epsilonproteobacteria (4), Alphaproteobacteria (6), Gammaproteobacteria (54) | 68   |
| NA             | 93 Different Classess                                                                                | 2848 |


[1]:https://webapp.ufz.de/marmdb/
Kasmanas, J. C., Bartholomäus, A., Corrêa, F. B., Tal, T., Jehmlich, N., Herberth, G., von Bergen, M., Stadler, P. F., de Carvalho, A. & da Rocha, U. N. (2021). HumanMetagenomeDB: a public repository of curated and standardized metadata for human metagenomes. Nucleic Acids Research, 49(D1), D743–D750.



Exploring strain diversity of dominant human skin bacterial species using single-cell genome sequencing
GAL08, an Uncultivated Group of Acidobacteria, Is a Dominant Bacterial Clade in a Neutral Hot Spring
Strain-level profiling of viable microbial community by selective single-cell genome sequencing
Single-cell genomics unveils a canonical origin of the diverse mitochondrial genomes of euglenozoans.
Single-cell genomics for resolution of conserved bacterial genes and mobile genetic elements of the human intestinal microbiota using flow.
Single-cell genomics of uncultured bacteria reveals dietary fiber responders in the mouse gut microbiota.
