import glob
import itertools
import math
import re

batchsize = 50
endingpunctuation = set(".!?")
minsyl = 14
maxsyl = 18
minrelfreq = 2/3
maxrelfreq = 3/2
mincommacount = 10
minmidpunctcount = 10

punctuation = endingpunctuation.union(",")

cmudict = {}
with open("cmudict/cmudict.dict") as f:
    for i in f.read().splitlines():
        i = i.partition(" #")[0].split(" ")
        if i[0][-1] != ")":
            cmudict[i[0]] = i[1:]

with open("frequencies.tsv") as f:
    goalfreqstemp = [i.split("\t") for i in f.read().splitlines()]
goalfreqssum = sum([int(i[1]) for i in goalfreqstemp])
goalfreqs = {i[0]: int(i[1])/goalfreqssum for i in goalfreqstemp}

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
        lines = [j for j in f.read().splitlines() if j]
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
                elif l[-1] in "012" or l in punctuation:
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
