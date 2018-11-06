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
        b = line.split(" ")[1]
        types.append(a)
        paths.append(b)
    return types, paths

if __name__ == "__main__":
    # f = open("train/Data/001/002", 'r', encoding='gbk')
    # doc = str(f.read())
    # s_doc = BeautifulSoup(doc, "lxml")
    # # print(s_doc.prettify())
    # print((s_doc.find("text").string))  # get text
    # # print(s_doc.find("subject").string) # get subject
    index_file = open(args.config, 'r')
    train_label, train_path = f(index_file)

    print(len(train_label), len(train_path))
