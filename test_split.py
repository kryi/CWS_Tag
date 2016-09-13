#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: 52nlpcn@gmail.com
# Copyright 2014 @ YuZhen Technology
#
# split chinese characters and add space between them

import codecs
import sys


def character_split(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        for word in line.strip():
            output_data.write(word + " ")
        output_data.write("\n")
    input_data.close()
    output_data.close()


if __name__ == '__main__':
    input_file = "icwb2-data\\testing\msr_test2.utf8"
    output_file = ".\output\\test_tagging.txt"
    character_split(input_file, output_file)
