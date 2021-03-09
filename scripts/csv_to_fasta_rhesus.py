#!/usr/bin/env python

"""
Extract rhesus sequences for one segment from the combined CSV file.
"""

import re
import sys
import csv
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

def load_csv(input_csv):
    with open(input_csv) as f_in:
        reader = csv.DictReader(f_in)
        rows = list(reader)
    return rows

def csv_to_fasta(segment, input_csv, output_fasta):
    rows = load_csv(input_csv)
    # Filter to selected segment and just rhesus
    is_rhesus = lambda r: int(r["ChinRhe"]) > 0 or int(r["IndiRhe"]) > 0
    rows = [row for row in rows if is_rhesus(row) and segment in row["Segment"]]
    with open(output_fasta, "wt") as f_out:
        for row in rows:
            SeqIO.write(
                SeqRecord(Seq(row["Seq"]), id=row["Allele"], description=""),
                f_out,
                "fasta-2line")

if __name__ == "__main__":
    csv_to_fasta(*sys.argv[1:])
