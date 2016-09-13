#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: 52nlpcn@gmail.com
# Copyright 2014 @ YuZhen Technology
#
# 4 tags for character tagging: B(Begin), E(End), M(Middle), S(Single)

# modify by hcs

import codecs
import sys
import os

from feature_extract import *

# def strQ2B(ustring):
#     """全角转半角"""
#     rstring = ""
#     for uchar in ustring:
#         inside_code = ord(uchar)
#         if inside_code == 12288:
#             inside_code = 32
#         elif (inside_code >= 65281 and inside_code <= 65374):
#             inside_code -= 0xfee0
#
#         rstring += chr(inside_code)
#     return rstring


def character_tagging(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():

        word_list = line.strip().split()

        for word in word_list:
            if len(word) == 1:
                output_data.write(word + "/S ")
            else:
                output_data.write(word[0] + "/B ")
                for w in word[1:len(word) - 1]:
                    output_data.write(w + "/M ")
                output_data.write(word[len(word) - 1] + "/E ")
        output_data.write("\n")
    input_data.close()
    output_data.close()


if __name__ == '__main__':
    input_file = "icwb2-data\\training\msr_training.utf8"
    output_file = ".\output\\train_tagging.txt"

    if not os.path.exists('.\output'):
        os.mkdir('.\output')
    character_tagging(input_file, output_file)