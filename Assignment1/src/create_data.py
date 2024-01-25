en_sentences = []
fa_sentences = []

with open('TED2020.en-fa.en', 'r', encoding="utf-8") as f:
    for line in f:
        if len(line.strip()) > 0:
            en_sentences.append(line.strip())
with open('TED2020.en-fa.fa', 'r', encoding="utf-8") as f:
    for line in f:
        if len(line.strip()) > 0:
            fa_sentences.append(line.strip())

with open('data.txt', 'a', encoding="utf-8") as f:
    for index, s in enumerate(en_sentences):
        f.write(s + " ||| " + fa_sentences[index] + "\n")