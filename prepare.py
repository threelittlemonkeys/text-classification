import sys
import re
from model import UNIT, PAD, UNK, PAD_IDX, UNK_IDX
from utils import tokenize

MIN_LEN = 5
MAX_LEN = 50

def load_data():
    data = []
    word_to_idx = {PAD: PAD_IDX, UNK: UNK_IDX}
    tag_to_idx = {}
    fo = open(sys.argv[1])
    for line in fo:
        x, y = line.split("\t")
        x = tokenize(x, UNIT if UNIT == "char" else "word")
        y = y.strip()
        if len(x) < MIN_LEN or len(x) > MAX_LEN:
            continue
        if UNIT == "char+word":
            x += list("".join(x))
        for w in x:
            if w not in word_to_idx:
                word_to_idx[w] = len(word_to_idx)
        if y not in tag_to_idx:
            tag_to_idx[y] = len(tag_to_idx)
        data.append([str(word_to_idx[w]) for w in x] + [str(tag_to_idx[y])])
    data.sort(key = len, reverse = True)
    fo.close()
    return data, word_to_idx, tag_to_idx

def save_data(data):
    fo = open(sys.argv[1] + ".csv", "w")
    for seq in data:
        fo.write(" ".join(seq) + "\n")
    fo.close()

def save_word_to_idx(word_to_idx):
    fo = open(sys.argv[1] + ".word_to_idx", "w")
    for word, _ in sorted(word_to_idx.items(), key = lambda x: x[1]):
        fo.write(word + "\n")
    fo.close()

def save_tag_to_idx(tag_to_idx):
    fo = open(sys.argv[1] + ".tag_to_idx", "w")
    for label, _ in sorted(tag_to_idx.items(), key = lambda x: x[1]):
        fo.write(label + "\n")
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s training_data" % sys.argv[0])
    data, word_to_idx, tag_to_idx = load_data()
    save_data(data)
    save_word_to_idx(word_to_idx)
    save_tag_to_idx(tag_to_idx)
