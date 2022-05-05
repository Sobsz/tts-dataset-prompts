from g2p_en import G2p
import glob
import itertools
import math
import re

batchsize = 50
endingpunctuation = set(".!?")
minsyl = 14
maxsyl = 18
minrelfreq = 1/2
maxrelfreq = 3/2
mincommacount = 10
minmidpunctcount = 10

phonemes = set(("AA0", "AA1", "AA2", "AE0", "AE1", "AE2", "AH0", "AH1", "AH2", "AO0", "AO1", "AO2", "AW0", "AW1", "AW2", "AY0", "AY1", "AY2", "B", "CH", "D", "DH", "EH0", "EH1", "EH2", "ER0", "ER1", "ER2", "EY0", "EY1", "EY2", "F", "G", "HH", "IH0", "IH1", "IH2", "IY0", "IY1", "IY2", "JH", "K", "L", "M", "N", "NG", "OW0", "OW1", "OW2", "OY0", "OY1", "OY2", "P", "R", "S", "SH", "T", "TH", "UH0", "UH1", "UH2", "UW0", "UW1", "UW2", "V", "W", "Y", "Z", "ZH"))
punctuation = endingpunctuation.union(",")

with open("frequencies.tsv") as f:
    goalfreqstemp = [i.split("\t") for i in f.read().splitlines()]
goalfreqssum = sum([int(i[1]) for i in goalfreqstemp])
goalfreqs = {i[0]: int(i[1])/goalfreqssum for i in goalfreqstemp}

g2p = G2p()

for i in glob.glob("*.txt"):
    print(f"checking {i}")
    with open(i) as f:
        lines = [j for j in f.read().splitlines() if j]
    if len(lines) % batchsize != 0:
        print(f"! last batch only has {len(lines) % batchsize} sentences")
    for j in range(math.ceil(len(lines)/batchsize)):
        print(f"- batch {j+1}")
        batchpre = lines[j*50 : min((j+1)*batchsize, len(lines))]
        batch = [g2p(k) for k in batchpre]

        sylgood = True
        for k in range(len(batch)):
            lineno = j*batchsize + k + 1
            sentence = batchpre[k]
            sylcount = 0
            if batch[k][-1] not in punctuation:
                print(f"! - line {lineno} doesn't end in punctuation: \"{sentence}\"")
                sylgood = False
                continue
            for l in batch[k][:-1]:
                if l[-1] in "012" or l in punctuation:
                    sylcount += 1
            if not (minsyl <= sylcount <= maxsyl):
                sylgood = False
                print(f"! - syllable count in line {lineno} is {sylcount}: \"{sentence}\"")
        if sylgood:
            print("- - syllable count check passed")

        batchchain = list(itertools.chain.from_iterable(batch))

        phonemecounts = {}
        for k in phonemes:
            phonemecounts[k] = batchchain.count(k)
        phonemefreqs = {k[0]: k[1] / len(batchchain) for k in phonemecounts.items()}
        phonemefreqsrelative = {k[0]: k[1] / goalfreqs[k[0]] for k in phonemefreqs.items()}
        notrepresented = []
        underrepresented = []
        underrepresented2 = []
        overrepresented = []
        for k in phonemefreqsrelative:
            if phonemefreqsrelative[k] < minrelfreq:
                if phonemefreqsrelative[k]:
                    underrepresented.append((k, phonemefreqsrelative[k]))
                else:
                    notrepresented.append(k)
            elif k[-1] not in "012" and phonemecounts[k] == 1:
                underrepresented2.append(k)
            elif phonemefreqsrelative[k] > maxrelfreq:
                if phonemecounts[k] > 4: # else some phonemes (e.g. `OY2`) wouldn't be allowed to be represented at all
                    overrepresented.append((k, phonemefreqsrelative[k]))
        if notrepresented:
            print(f"! - these phonemes are not represented: {', '.join(sorted(notrepresented))}")
        if underrepresented2:
            print(f"! - these consonants are only represented once: {', '.join(sorted(notrepresented))}")
        if underrepresented:
            print(f"! - these phonemes are underrepresented: {', '.join(f'{k[0]} ({k[1]:.3f}, {phonemecounts[k[0]]})' for k in sorted(underrepresented, key = lambda a: a[1]))}")
        if overrepresented:
            print(f"! - these phonemes are overrepresented: {', '.join(f'{k[0]} ({k[1]:.3f}, {phonemecounts[k[0]]})' for k in sorted(overrepresented, key = lambda a: a[1], reverse = True))}")
            print("- - here are some sentences containing them:")
            for k in overrepresented:
                print(f"- - - {k[0]}")
                for l in range(len(batch)):
                    if k[0] in batch[l]:
                        print(f"- - - {batchpre[l]}")
        if not notrepresented and not underrepresented and not underrepresented2 and not overrepresented:
            print("- - representation check passed")
            pfrs = sorted(phonemefreqsrelative.items(), key = lambda a: a[1])
            print(f"- - closest to underrepresentation: {', '.join(f'{k[0]} ({k[1]:.3f}, {phonemecounts[k[0]]})' for k in pfrs[:5])}")
            print(f"- - closest to overrepresentation: {', '.join(f'{k[0]} ({k[1]:.3f}, {phonemecounts[k[0]]})' for k in pfrs[:-11:-1])}")
        commacount = 0
        midpunctcount = 0
        for k in batch:
            if "," in k:
                commacount += 1
            if not endingpunctuation.isdisjoint(k[:-1]):
                midpunctcount += 1
        if commacount >= mincommacount:
            print("- - comma count check passed")
        else:
            print(f"! - not enough commas, {mincommacount - commacount} more required")
        if midpunctcount >= minmidpunctcount:
            print("- - mid-line punctuation count check passed")
        else:
            print(f"! - not enough mid-line punctuation, {minmidpunctcount - midpunctcount} more required")

print("checked all")
