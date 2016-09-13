#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: houchengshang@gmail.com

import math
from collections import deque


class Corpus(object):
    def __init__(self, filepath):
        self.text = []  # text
        self.word = {}
        self.history = {}
        self.frequency = {}

        with open(filepath, 'r', encoding='utf-8') as fp:
            self.text = fp.readlines()
        self.text = [x.rstrip() for x in self.text]

    def data_print(self):
        for x in self.text:
            print(x)

    def word_print(self):
        for x, y in self.word.items():
            print(x, y)

    def history_print(self):
        for x, y in self.history.items():
            print(x, y)

    def data2dict(self):
        self.word["<EOS2>"] = 0
        self.word["<EOS1>"] = 0
        self.word["<BOS1>"] = 0
        self.word["<BOS2>"] = 0
        for x in self.text:
            words = iter(x.split())
            for word in words:
                assert isinstance(word, str), print(word)
                if word in self.word:
                    self.word[word] += 1
                else:
                    self.word[word] = 1
            self.word["<EOS2>"] += 1
            self.word["<EOS1>"] += 1
            self.word["<BOS1>"] += 1
            self.word["<BOS2>"] += 1

    def data2history(self):

        for x in self.text:
            n1 = "<BOS1>"
            n2 = "<BOS2>"
            words = iter(x.split())
            for n3 in words:
                # print(n1, n2, n3)
                if (n1, n2, n3) in self.history:
                    self.history[(n1, n2, n3)] += 1
                else:
                    self.history[(n1, n2, n3)] = 1
                n1 = n2
                n2 = n3
            if (n1, n2, "<EOS2>") in self.history:
                self.history[(n1, n2, "<EOS2>")] += 1
            else:
                self.history[(n1, n2, "<EOS2>")] = 1
            if (n2, "<EOS2>", "<EOS1>") in self.history:
                self.history[(n2, "<EOS2>", "<EOS1>")] += 1
            else:
                self.history[(n2, "<EOS2>", "<EOS1>")] = 1

    def compute_frequency(self):
        for x, y in self.history.items():
            self.frequency[x] = y / self.word[x[-1]]
            # for x, y in self.frequency.items():
            #     print(x, y)


class WordSegment(object):
    def __init__(self):
        self.sentence = ""
        self.DAG = {}
        self.result = []

    def get_sentence(self, sentence):
        if not isinstance(sentence, str):
            print("not a string")
            raise TypeError
        self.sentence = sentence
        print("input sentence is :",self.sentence)

    def get_dag(self, words):
        for k in range(0, len(self.sentence)):
            temlist = []  # position of word segment 0: 0,1,2
            for i in range(k, len(self.sentence)):  # should be max words length
                subsentence = self.sentence[k:i + 1]
                if subsentence in words:
                    temlist.append(i)
            if not temlist:
                temlist.append(k)
            self.DAG[k] = temlist

    def search_segment(self, corpus):
        def mk_dict(ty, tz):
            return {'path': ty, 'pos': tz}

        def compute_probability(path,max_value):
            ret = 0
            # path.append("<EOS2>", "<EOS1>")
            n1 = "<BOS1>"
            n2 = "<BOS2>"
            word_size = len(corpus.word)
            history = list(corpus.history.keys())
            for n3 in path:
                if (n1, n2, n3) in history:
                    ret += math.log(corpus.frequency[(n1, n2, n3)])
                else:
                    ret -= math.log(word_size)
                if max_value > ret:
                    break
            return ret

        queue = deque([mk_dict([], 0)])  # (prob,path,pos)
        sen_len = len(self.sentence)
        max_value = -1000000
        while queue:
            cur_node = queue.popleft()
            if sen_len == cur_node['pos']:
                cur_proba = compute_probability(cur_node['path'],max_value)
                print("path",cur_node['path'],"probability",cur_proba)
                if cur_proba > max_value:
                    max_value = cur_proba
                    self.result = cur_node['path']
                continue

            l = cur_node['pos']
            next_word = self.DAG[l]
            # print("pos next_word",l,next_word)
            append_word = 1
            for r in next_word:
                # print(self.sentence[l:r + 1])
                if self.sentence[l:r + 1] in list(corpus.word.keys()):
                    append_word = 0
                    y = [x for x in cur_node['path']]
                    y.append(self.sentence[l:r + 1])
                    z = r + 1
                    # print("cur_path",y)
                    queue.append(mk_dict(y, z))
            if append_word:
                y = [x for x in cur_node['path']]
                y.append(self.sentence[l])
                z = l + 1
                # print("cur_path",y)
                queue.append(mk_dict(y, z))

        print(self.result)


if __name__ == '__main__':
    f = Corpus(r'C:\Users\hou\PycharmProjects\CWS_Tag\icwb2-data\training\msr_training.utf8')
    f.data2dict()
    f.data2history()
    # f.history_print()
    f.compute_frequency()

    ws = WordSegment()
    test = Corpus(r'C:\Users\hou\PycharmProjects\CWS_Tag\icwb2-data\testing\msr_test2.utf8')
    for x in test.text:
        ws.get_sentence(x)
        ws.get_dag(list(f.word.keys()))
        print("dag ", ws.DAG)
        ws.search_segment(f)
