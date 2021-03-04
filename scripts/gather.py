#!/usr/bin/env python

"""
Gather all the info for one segment (V, D, or J) and write to a single CSV.
"""

import sys
import csv
from Bio import SeqIO

def gather(
        input_csv, input_fasta_rhesus, input_fasta_cynomolgus, input_validated_rhesus, input_validated_cynomolgus,
        output_csv):
    """Gather all the info for one segment (V, D, or J) and write to a single CSV.

    The arguments are all file paths:
    input_csv: existing CSV from Table S5
    input_fasta_rhesus: FASTA sequences for rhesus
    input_fasta_cynomolgus: FASTA sequences for cynomolgus
    input_validated_rhesus: text file listing validated seqs for rhesus from Table S3/S4
    input_validated_cynomolgus: text file listing validated seqs for cynomolgus from Table S3/S4
    output_csv: path for output CSV file
    """
    # CSV version of a sheet from Table S5
    with open(input_csv) as f_in:
        reader = csv.DictReader(f_in)
        allele_attrs = list(reader)
    # Rhesus and Cynomolgus are separate FASTA files but there are some shared
    # alleles.  We'll merge both sets into one dictionary keyed on Sequence ID.
    # Sequences should be identical for any identical seq IDs, obviously.
    with open(input_fasta_rhesus) as f_in:
        seqs = {record.id: str(record.seq) for record in SeqIO.parse(f_in, "fasta")}
    with open(input_fasta_cynomolgus) as f_in:
        seqs_cyno = {record.id: str(record.seq) for record in SeqIO.parse(f_in, "fasta")}
    common_keys = set(seqs.keys()) & set(seqs_cyno.keys())
    if any([seqs[key] != seqs_cyno[key] for key in common_keys]):
        raise ValueError("disagreement between seq IDs for rhesus and cynomolgus")
    seqs.update(seqs_cyno)
    # So those two sets are consistent.  Is the combination a 1:1  match with
    # the S5 info?
    allele_attrs_set = {row["Alleles"] for row in allele_attrs}
    seqs_set = set(seqs.keys())
    if allele_attrs_set != seqs_set:
        sys.stderr.write("Mismatch between FASTA and S5\n")
        seqs_only = seqs_set - allele_attrs_set
        allele_attrs_only = allele_attrs_set - seqs_set
        if seqs_only:
            sys.stderr.write("Only in FASTA: %s\n" % str(seqs_only))
        if allele_attrs_only:
            sys.stderr.write("Only in S5: %s\n" % str(allele_attrs_only))
    # Table S3/S4 give lists of genomically validated alleles.  The same info
    # is in a column in S5 for V, though.
    with open(input_validated_rhesus) as f_in:
        validated_rhesus = {line.strip() for line in f_in}
    with open(input_validated_cynomolgus) as f_in:
        validated_cynomolgus = {line.strip() for line in f_in}
    is_rhesus = lambda row: int(row["ChinRhe"]) > 0 or int(row["IndiRhe"]) > 0
    is_cyno = lambda row: int(row["IndoCyn"]) > 0 or int(row["MaurCyn"]) > 0
    if "Genomically validated" in allele_attrs[0].keys():
        is_validated = lambda row: row["Genomically validated"] == "T"
        validated_rhesus_attrs = {row["Alleles"] for row in allele_attrs if is_validated(row) and is_rhesus(row) }
        validated_cyno_attrs = {row["Alleles"] for row in allele_attrs if is_validated(row) and is_cyno(row) }
        if validated_rhesus_attrs != validated_rhesus:
            sys.stderr.write("Mismatch between S5 and validated rhesus list\n")
            list_only = validated_rhesus - validated_rhesus_attrs
            attrs_only = validated_rhesus_attrs - validated_rhesus
            if list_only:
                sys.stderr.write("Only in validated rhesus list: %s\n" % str(list_only))
            if attrs_only:
                sys.stderr.write("Only in S5 validated rhesus set: %s\n" % str(attrs_only))
    else:
        boolify = lambda val: "T" if val else "F"
        for row in allele_attrs:
            if is_rhesus(row):
                row["Genomically validated"] = boolify(row["Alleles"] in validated_rhesus)
            elif is_cyno(row):
                row["Genomically validated"] = boolify(row["Alleles"] in validated_cynomolgus)


    for row in allele_attrs:
        row["Seq"] = seqs.get(row["Alleles"], "")
    with open(output_csv, "wt") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=allele_attrs[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(allele_attrs)

if __name__ == "__main__":
    gather(*sys.argv[1:])
