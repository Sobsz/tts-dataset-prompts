import re

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

counts = {i: 0 for i in phonemes}

with open("corpus.txt", encoding = "utf-8") as f:
    a = re.sub(r'[^\w-]', ' ', f.read()).lower()
    for i in a.split():
        if i in cmudict:
            for j in cmudict[i]:
                counts[j] += 1

with open("frequencies.tsv", "w") as f:
    f.write("\n".join([f"{i[0]}\t{i[1]}" for i in sorted(counts.items(), key = lambda a: a[1], reverse = True)]))
