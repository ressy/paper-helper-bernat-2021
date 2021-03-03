#!/usr/bin/env python

import sys
import csv
from Bio import SeqIO

def gather(input_csv, input_rhesus, input_cynomolgus, output_csv):
    with open(input_rhesus) as f_in:
        seqs = {record.id: str(record.seq) for record in SeqIO.parse(f_in, "fasta")}
    with open(input_cynomolgus) as f_in:
        seqs_cyno = {record.id: str(record.seq) for record in SeqIO.parse(f_in, "fasta")}
    common_keys = set(seqs.keys()) & set(seqs_cyno.keys())
    if any([seqs[key] != seqs_cyno[key] for key in common_keys]):
        raise ValueError("disagreement between seq IDs for rhesus and cynomolgus")
    seqs.update(seqs_cyno)
    rows = []
    with open(input_csv) as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            row["Seq"] = seqs.get(row["Alleles"], "")
            rows.append(row)
    with open(output_csv, "wt") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    gather(*sys.argv[1:])
