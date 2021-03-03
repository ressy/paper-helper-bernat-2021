from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

wildcard_constraints:
    segment="[VDJ]"

rule all:
    input: expand("output/{segment}.csv", segment = ["V", "D", "J"])

rule gather_alleles_V:
    output: "output/V.csv"
    input:
        csv="parsed/S5A.csv",
        rhesus="from-website/rhesus.V.fasta",
        cynomolgus="from-website/cynomolgus.V.fasta"
    shell: "./scripts/gather.py {input.csv} {input.rhesus} {input.cynomolgus} {output}"

rule gather_alleles_D:
    output: "output/D.csv"
    input:
        csv="parsed/S5D.csv",
        rhesus="from-website/rhesus.D.fasta",
        cynomolgus="from-website/cynomolgus.D.fasta"
    shell: "./scripts/gather.py {input.csv} {input.rhesus} {input.cynomolgus} {output}"

rule gather_alleles_J:
    output: "output/J.csv"
    input:
        csv="parsed/S5E.csv",
        rhesus="from-website/rhesus.J.fasta",
        cynomolgus="from-website/cynomolgus.J.fasta"
    shell: "./scripts/gather.py {input.csv} {input.rhesus} {input.cynomolgus} {output}"

rule extract_s5:
    output: expand("parsed/S5{sheet}.csv", sheet=["A", "B", "C", "D", "E"])
    input: "from-paper/tableS5.xlsx"
    shell: "./scripts/extract_s5.py {input}"

rule download_segment_rhesus:
    input: HTTP.remote("http://kimdb.gkhlab.se/datasets/Macaca%20mulatta/Ig/Heavy/{segment}")
    output: "from-website/rhesus.{segment}.fasta"
    shell: "cp {input} {output}"

rule download_segment_cynomolgus:
    input: HTTP.remote("http://kimdb.gkhlab.se/datasets/Macaca%20fascicularis/Ig/Heavy/{segment}")
    output: "from-website/cynomolgus.{segment}.fasta"
    shell: "cp {input} {output}"
