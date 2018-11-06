from bs4 import BeautifulSoup
import numpy as np
import argparse
import re
import jieba
import pickle
from collections import Counter
import tqdm

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--config', default="final_train_index.txt")
parser.add_argument('--spam_config', default="index/spam.txt")
parser.add_argument('--ham_config', default="index/ham.txt")

parser.add_argument('--spam_dict', default='pickle/spam.pickle')
parser.add_argument('--ham_dict', default='pickle/ham.pickle')

args = parser.parse_args()


def info(file):
    types = []
    paths = []
    for line in file.readlines():
        a = line.split(" ")[0]
        b = line.split(" ")[1].strip('\n')
        types.append(a)
        paths.append(b)
    return types, paths


def delete_punc(origin):
    trimed = re.sub(
        "[\s+\.\!\/_,$%^*():+\"\'-=?]+|[+——！，。？、~@#￥%……&*（）“”【】：]+", " ", origin)
    return trimed


def get_text(email_file):
    doc = str(email_file.read())
    s_doc = BeautifulSoup(doc, 'lxml')
    text_body = s_doc.find("text")
    # print(text_body)
    text_body = str(text_body).strip('<text>').strip('</text>')
    return (delete_punc(text_body))


if __name__ == "__main__":

    spam_file = open(args.spam_config, 'r')
    ham_file = open(args.ham_config, 'r')
    spam_types, spam_paths = info(spam_file)
    ham_types, ham_paths = info(ham_file)
    # print(len(spam_types), len(spam_paths))
    print(len(ham_types), len(ham_paths))

    spams = []
    hams = []

    for i in tqdm.trange(len(spam_paths)):
        with open(spam_paths[i], 'r', encoding='utf-8', errors='ignore') as email:
            # print(spam_paths[i])
            t = jieba.lcut(get_text(email))
            # t = set(text_segmentation_result)
            t = [x for x in t if x != ' ']
            spams += t
    spams_counter = Counter(spams)

    with open(args.spam_dict, 'wb') as sf:
        pickle.dump(spams_counter, sf)

    for i in tqdm.trange(len(ham_paths)):
        with open(ham_paths[i], 'r', encoding='utf-8', errors='ignore') as email:
            # print(ham_paths[i])
            t = jieba.lcut(get_text(email))
            t = [x for x in t if x != ' ']
            hams += t

    hams_counter = Counter(hams)

    with open(args.ham_dict, 'wb') as hf:
        pickle.dump(hams_counter, hf)

