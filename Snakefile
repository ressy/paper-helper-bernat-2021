rule gather_alleles:
    output: "output/alleles.csv"
    input:
        ighv="parsed/S5A.csv",
        ighd="parsed/S5D.csv",
        ighj="parsed/S5E.csv"

rule extract_s5:
    output: expand("parsed/S5{sheet}.csv", sheet=["A", "B", "C", "D", "E"])
    input: "from-paper/tableS5.xlsx"
    shell: "./scripts/extract_s5.py {input}"
