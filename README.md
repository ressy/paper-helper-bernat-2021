# Data Gathering from Bernat 2021

Some scripts to aggregate antibody sequences and results metadata from:

Vázquez Bernat, Néstor et al.  Rhesus and cynomolgus macaque immunoglobulin heavy-chain genotyping yields comprehensive databases of germline VDJ alleles.  Immunity, Volume 54, Issue 2, 355 - 366.e4 <https://doi.org/10.1016/j.immuni.2020.12.018>

Final combined output is in [output/alleles.csv](output/alleles.csv).

## Data Sources

Final allele sequences, straight from the source: <http://kimdb.gkhlab.se/datasets/>

GenBank accession ranges, for final allele sequences:

 * MT561887-MT563069
 * MT643213-MT643227
 * MT672244-MT672249
 * MT542339-MT542468
 * MT643195-MT643212
 * MT643228-MT643233

(Not currently drawing from those except for MT643227 to supply
`IGHV4-149*01_S1940`.)

ENA accession ranges, for read libraries:

 * ERR4250665-ERR4250672
 * ERR4238026-ERR4238115

### Tables

Used here:

 * S3: lists of validated IGHD and IGHJ alleles, by species
 * S4: lists of validated IGHV alleles, by species
 * S5A: IGHV alleles (all)
 * S5B: IGHV alleles (rhesus)
 * S5C: IGHV alleles (cynomolgus)
 * S5D: IGHD alleles
 * S5E: IGHJ alleles

Not used here:

 * S1A: 5' RACE primers
 * S1B: 5' MPTX primers
 * S6A: IGHV genomic validation primers
 * S6B: IGHD genomic validation primers
 * S6C: IGHJ genomic validation primers
