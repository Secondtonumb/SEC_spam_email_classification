from bs4 import BeautifulSoup
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--config', default="final_train_index.txt")

args = parser.parse_args()


def f(file):
    types = []
    paths = []
    for line in file.readlines():
        a = line.split(" ")[0]
        b = line.split(" ")[1].strip('\n')
        types.append(a)
        paths.append(b)
    return types, paths

def get_text(email_file):
    doc = str(email_file.read())
    s_doc = BeautifulSoup(doc, 'lxml')
    return (s_doc.find("text").string)

if __name__ == "__main__":
    # f = open("train/Data/001/002", 'r', encoding='gbk')

    index_file = open(args.config, 'r')
    train_label, train_path = f(index_file)
    print(len(train_label), len(train_path))
    print(train_label)

    for i in range(10):
        with open(train_path[i], 'r', encoding='gbk') as email_file:
            print(get_text(email_file))
