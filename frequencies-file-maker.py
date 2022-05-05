from g2p_en import G2p
import re

phonemes = set(("AA0", "AA1", "AA2", "AE0", "AE1", "AE2", "AH0", "AH1", "AH2", "AO0", "AO1", "AO2", "AW0", "AW1", "AW2", "AY0", "AY1", "AY2", "B", "CH", "D", "DH", "EH0", "EH1", "EH2", "ER0", "ER1", "ER2", "EY0", "EY1", "EY2", "F", "G", "HH", "IH0", "IH1", "IH2", "IY0", "IY1", "IY2", "JH", "K", "L", "M", "N", "NG", "OW0", "OW1", "OW2", "OY0", "OY1", "OY2", "P", "R", "S", "SH", "T", "TH", "UH0", "UH1", "UH2", "UW0", "UW1", "UW2", "V", "W", "Y", "Z", "ZH"))
counts = {i: 0 for i in phonemes}

g2p = G2p()
with open("corpus.txt", encoding = "utf-8") as f:
    a = g2p(f.read().replace("\n", " "))
    for i in a:
        if i in phonemes:
            counts[i] += 1

with open("frequencies.tsv", "w") as f:
    f.write("\n".join([f"{i[0]}\t{i[1]}" for i in sorted(counts.items(), key = lambda a: a[1], reverse = True)]))
