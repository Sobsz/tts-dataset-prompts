import glob
import itertools
import math
import re

batchsize = 50
endingpunctuation = set(".!?")
minsyl = 14
maxsyl = 18
mincommacount = 10
minmidpunctcount = 10

punctuation = endingpunctuation.union(",")

cmudict = {}
with open("cmudict/cmudict.dict") as f:
    for i in f.read().splitlines():
        i = i.partition(" #")[0].split(" ")
        if i[0][-1] != ")":
            cmudict[i[0]] = i[1:]

phonemes = set()
with open("cmudict/cmudict.phones") as f:
    for i in f.read().splitlines():
        i = i.split("\t")
        if i[1] == "vowel":
            phonemes.update((i[0]+"0", i[0]+"1", i[0]+"2"))
        else:
            phonemes.add(i[0])

for i in glob.glob("*.txt"):
    print(f"checking {i}")
    with open(i) as f:
        lines = f.read().splitlines()
    if len(lines) % batchsize != 0:
        print(f"! last batch only has {len(lines) % batchsize} sentences")
    for j in range(math.ceil(len(lines)/batchsize)):
        print(f"- batch {j+1}")
        batchpre = lines[j*50 : min((j+1)*batchsize, len(lines))]
        batch = []
        for k in batchpre:
            split = re.findall(r"[\w']+|[.,!?;]", k.lower())
            split = [cmudict.get(l, [l] if l in punctuation else ["[UNK]"]) for l in split]
            batch.append(list(itertools.chain.from_iterable(split)))

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
                if l == "[UNK]":
                    print(f"! - unknown word in line {lineno}: \"{sentence}\"")
                    break
                elif l[-1] in ("0", "1", "2"):
                    sylcount += 1
                elif l in ".,!?;":
                    sylcount += 2
            if not (minsyl <= sylcount <= maxsyl):
                sylgood = False
                print(f"! - syllable count in line {lineno} is {sylcount}: \"{sentence}\"")
        if sylgood:
            print("- - syllable count check successful")

        batchchain = list(itertools.chain.from_iterable(batch))
        
        missingphonemes = phonemes.difference(batchchain)
        if missingphonemes:
            print(f"! - the following phonemes are not represented: {', '.join(sorted(missingphonemes))}")
        else:
            print("- - phoneme coverage check successful")

        phonemecounts = {}
        for k in phonemes:
            phonemecounts[k] = batchchain.count(k)
        report = [f"{k[0]} ({k[1]})" for k in sorted(phonemecounts.items(), key = lambda a: a[1])[:10]]
        print(f"- - least represented phonemes: {', '.join(report)}")
        

        commacount = 0
        midpunctcount = 0
        for k in batch:
            if "," in k:
                commacount += 1
            if not endingpunctuation.isdisjoint(k[:-1]):
                midpunctcount += 1
        if commacount >= mincommacount:
            print("- - comma count check successful")
        else:
            print(f"! - not enough commas, {mincommacount - commacount} more required")
        if midpunctcount >= minmidpunctcount:
            print("- - mid-line punctuation count check successful")
        else:
            print(f"! - not enough mid-line punctuation, {minmidpunctcount - midpunctcount} more required")

print("checked all")
