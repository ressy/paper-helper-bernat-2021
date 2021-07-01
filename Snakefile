from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

from csv import DictReader

with open("SraRunTable.txt") as f_in:
    reader = DictReader(f_in)
    SRA = list(reader)

HTTP = HTTPRemoteProvider()

wildcard_constraints:
    segment="[VDJ]"

rule combine_output:
    output: "output/alleles.csv"
    input:
        v="output/V.csv",
        d="output/D.csv",
        j="output/J.csv",
        gbf="from-genbank/MT643227.1.gbf" # To fill in missing entry for IGHV4-149*01_S1940
    shell: "./scripts/combine_all.py {input.v} {input.d} {input.j} {input.gbf} {output}"

rule output_rhesus_fasta_by_segment:
    output: "output/rhesus_alleles.{segment}.fasta"
    input: "output/alleles.csv"
    shell: "./scripts/csv_to_fasta_rhesus.py {wildcards.segment} {input} {output}"

rule gather_alleles_V:
    output: "output/V.csv"
    input:
        csv="parsed/S5A.csv",
        fasta_rhesus="from-website/rhesus.V.fasta",
        fasta_cynomolgus="from-website/cynomolgus.V.fasta",
        validated_rhesus="from-paper/tableS4_rhesus.txt",
        validated_cynomolgus="from-paper/tableS4_cynomolgus.txt"
    # (Could also explicitly double-check S5A versus S5B + S5C, but they do match up.)
    shell: "./scripts/gather.py {input.csv} {input.fasta_rhesus} {input.fasta_cynomolgus} {input.validated_rhesus} {input.validated_cynomolgus} {output}"

rule gather_alleles_D:
    output: "output/D.csv"
    input:
        csv="parsed/S5D.csv",
        fasta_rhesus="from-website/rhesus.D.fasta",
        fasta_cynomolgus="from-website/cynomolgus.D.fasta",
        validated_rhesus="from-paper/tableS3_rhesus_d.txt",
        validated_cynomolgus="from-paper/tableS3_cynomolgus_d.txt"
    shell: "./scripts/gather.py {input.csv} {input.fasta_rhesus} {input.fasta_cynomolgus} {input.validated_rhesus} {input.validated_cynomolgus} {output}"

rule gather_alleles_J:
    output: "output/J.csv"
    input:
        csv="parsed/S5E.csv",
        fasta_rhesus="from-website/rhesus.J.fasta",
        fasta_cynomolgus="from-website/cynomolgus.J.fasta",
        validated_rhesus="from-paper/tableS3_rhesus_j.txt",
        validated_cynomolgus="from-paper/tableS3_cynomolgus_j.txt"
    shell: "./scripts/gather.py {input.csv} {input.fasta_rhesus} {input.fasta_cynomolgus} {input.validated_rhesus} {input.validated_cynomolgus} {output}"

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

rule all_sra_fastq:
    input: expand("from-sra/{srr}_{rp}.fastq.gz", srr=[row["Run"] for row in SRA], rp=[1, 2])

rule sra_fastq:
    output: expand("from-sra/{{srr}}_{rp}.fastq.gz", rp=[1, 2])
    shell: "fastq-dump  --split-files --gzip {wildcards.srr} --outdir from-sra"
