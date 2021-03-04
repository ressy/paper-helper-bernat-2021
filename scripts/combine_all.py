#!/usr/bin/env python

"""
Combine V, D, and J into one central allele table.

This also parses out antibody gene, family, etc. from the Allele name.
"""

import re
import sys
import csv
from Bio import SeqIO

def load_csv(input_csv):
    with open(input_csv) as f_in:
        reader = csv.DictReader(f_in)
        rows = list(reader)
    return rows

def combine_all(input_v, input_d, input_j, input_gbf, output_csv):
    """Combine V, D, and J into one central allele table."""
    rows_v = load_csv(input_v)
    rows_d = load_csv(input_d)
    rows_j = load_csv(input_j)
    # Single GenBank file for a missing sequence from the web FASTA
    gbf = SeqIO.read(input_gbf, "genbank")
    for row in rows_v:
        if row["Alleles"] == "IGHV4-149*01_S1940" and row["Seq"] == "":
            row["Seq"] = str(gbf.seq)
            break
    # Placeholders for not-applicable entries for D and J
    for row in rows_d + rows_j:
        row["Previous databases"] = ""
        row["Genomic assemblies"] = ""
    # Combine and add columns.  (Clearing the dict and appending the old items
    # lets us re-order while keeping the same object.)
    rows = rows_v + rows_d + rows_j
    for row in rows:
        row_old = row.copy()
        row.clear()
        row["Allele"] = row_old["Alleles"]
        del row_old["Alleles"]
        row["Gene"] = re.sub(r"\*.*$", "", row["Allele"])
        row["Gene"] = re.sub("NL_", "", row["Gene"])
        row["Family"] = re.sub("-.*", "", row["Gene"])
        row["Segment"] = row["Family"][:4]
        row["Locus"] = row["Segment"][:3]
        # A special case for IGHV, encoded in their allele names
        row["NotLinked"] = ""
        if row["Segment"] == "IGHV":
            if "NL_" in row["Allele"]:
                row["NotLinked"] = "T"
            else:
                row["NotLinked"] = "F"
        row.update(row_old)
    # write
    with open(output_csv, "wt") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=rows_v[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows_v + rows_d + rows_j)

if __name__ == "__main__":
    combine_all(*sys.argv[1:])
