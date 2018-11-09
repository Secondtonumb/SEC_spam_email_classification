from bs4 import BeautifulSoup
import argparse
import numpy as np
import re
import jieba
import pickle
from collections import Counter
import tqdm

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--test_config', default="test_index.txt")
args = parser.parse_args()


def get_path(f):
    paths = []
    for line in f.readlines():
        paths += line.split()
    return paths


def delete_punc(origin):
    trimed = re.sub(
        "[<>\\.\!\/_,$%^*():+\"\'-=?{}]+|[+——！，。？、~@#￥%……&*（）“”【】：]+", "", origin)
    return trimed


def get_text(email_file):
    doc = str(email_file.read())
    s_doc = BeautifulSoup(doc, 'lxml')
    text_body = s_doc.find("text")
    # print(text_body)
    text_body = str(text_body).strip('<text>').strip('</text>')
    return (delete_punc(text_body))

def get_vec_2(email_vocab, counter):
    p_arr = np.zeros(len(email_vocab), dtype=int)
    for i in range(len(email_vocab)):
        if counter[email_vocab[i]] == 0:
            p_arr[i] = 0
        else:            
            # if counter[email_vocab[i]] > 100: # if occurring time too much ,consider it as a noise
            #     p_arr[i] = 1
            # else:
            p_arr[i] = 1
    return p_arr 
            

if __name__ == "__main__":

    test_file = open(args.test_config, 'r')

    test_paths = get_path(test_file)

    test_num = len(test_paths)
    # test_num = 10

    with open('pickle/spam.pickle', 'rb') as sd:
        spam_dict = pickle.load(sd)
    sl = spam_dict
    
    with open('pickle/ham.pickle', 'rb') as hd:
        ham_dict = pickle.load(hd)
    hl = ham_dict

    dic_len = len(set(list(sl) + list(hl)))

    # spam_cnt_mat = np.zeros([test_num])
    # ham_cnt_mat = np.zeros([test_num])
    # spam_prob = np.zeros(test_num)
    # ham_prob = np.zeros(test_num)

    res = []
    
    for i in tqdm.trange(test_num):
        with open(test_paths[i], 'r',
                  encoding='utf-8',
                  errors='ignore') as email:
            # print(spam_paths[i])
            t = jieba.lcut(get_text(email), HMM=True)
            t = [x for x in t if x != ' ']
            t = [x for x in t if x != '\n']

            s_cnt = get_vec_2(t, sl)
            h_cnt = get_vec_2(t, hl)

            s_prob = sum(s_cnt)
            h_prob = sum(h_cnt)
            res.append(s_prob - h_prob > 0)
            
    # print(spam_cnt_mat, ham_cnt_mat)

    # spam_prob = 27494 / 37700 * spam_cnt_mat / (len(sl))
    # ham_prob = 10190 / 37700 * ham_cnt_mat / (len(hl))

    # spam_prob = spam_cnt_mat / (dic_len)
    # ham_prob = ham_cnt_mat / (dic_len)

    # res = spam_prob - ham_prob

    # print(res)
    
    res_list = []
    for i in range(len(res)):
        if res[i] == 0:
            res_list.append("spam")
        else:
            res_list.append("ham")

    with open('result/result', 'w') as f:
        for item in res_list:
            f.write('%s\n' % (item))

    print(res_list)
