"""
write by hcs
"""

import codecs

feat_dict = {}
tag_dict = {}


def split_pos(s):
    """
    split out word and pos in s into two separate lists
    """
    w = []
    pos = []
    # for i, t in enumerate(s):
    for i in range(len(s)):
        t = s[i]
        ind = t.rindex('/')
        w.append(t[:ind])
        pos.append(t[ind + 1:])
    return w, pos


def gather_feature(word, context, pos):
    if word in tag_dict:
        if pos not in tag_dict[word]:
            tag_dict[word][pos] = 1
        else:
            tag_dict[word][pos] += 1
    else:
        tag_dict[word] = {pos: 1}

    for pred in context:
        f = pred + '_' + pos
        feat_dict[f] = feat_dict.get(f, 0) + 1


def feature_b(words, pos, i):
    """
        The current character ( C0 )
    :param words: chinese character
    :param pos: part of speech
    :param i:
    :return: string of feature
    """
    return words[i]


def feature_c(words, pos, i):
    """
        The previous(next) two character ( -2,-1,1,2 )
    :param words:
    :param pos:
    :param i:
    :return:
    """
    l = len(words)
    if i > 1:
        c1 = words[i - 2]
    else:
        c1 = 'b'

    if i > 0:
        c2 = words[i - 1]
    else:
        c2 = 'b'
    if i < l - 1:
        c3 = words[i + 1]
    else:
        c3 = 'b'
    if i < l - 2:
        c4 = words[i + 2]
    else:
        c4 = 'b'

    return c1 + '_' + c2 + '_' + c3 + '_' + c4


def feature_d(words, pos, i):
    """
        The current character ( -1,0,0,1 )
    :param words: chinese character
    :param pos: part of speech
    :param i:
    :return: string of feature
    """
    l = len(words)
    if i > 0:
        c1 = words[i - 1]
    else:
        c1 = 'b'
    if i < l - 1:
        c3 = words[i + 1]
    else:
        c3 = 'b'

    return c1 + words[i] + words[i] + c3


def feature_e(words, pos, i):
    """
        The current character ( -2,-1 )
    :param words: chinese character
    :param pos: part of speech
    :param i:
    :return: string of feature
    """
    l = len(words)
    if i > 1:
        c1 = words[i]
    else:
        c1 = 'b'

    if i > 0:
        c2 = words[i - 1]
    else:
        c2 = 'b'
    return c1 + c2


def feature_f(words, pos, i):
    """
        The tag of character ( t-1,t-2 )
    :param words: chinese character
    :param pos: part of speech
    :param i:
    :return: string of feature
    """
    if i > 1:
        t1 = pos[i - 1]
    else:
        t1 = "_bd"

    if i > 2:
        t2 = pos[i - 2]
    else:
        t2 = '_bd'

    return 'tag' + t2 + t1


def feature_extract(file, func):
    """extract special features for rare word if rare_feat is True
    :param func:
    :param file:
    """
    context_cnt = []
    lines = 0
    for s in file:
        lines += 1
        if lines % 1000 == 0:
            print('%d lines' % lines)
        sent = s.split()
        if len(sent) == 0:
            continue
        # print(sent)
        words, pos = split_pos(sent)
        n = len(words)

        for i in range(n):
            context = []
            context_cnt.append(feature_c(words, pos, i) + '_' + pos[i] + '_' + words[i])
            # context.append(feature_c(words, pos, i))
            # context.append(feature_d(words, pos, i))
            # context.append(feature_e(words, pos, i))
            # context.append(feature_f(words, pos, i))
            # func(words[i], context, pos[i])
    with open("output\context.txt", 'w') as f:
        for x in context_cnt:
            print(x, file=f)
    return feat_dict


def save_features(filename):
    with open(filename, 'w') as f:
        for feat in feat_dict.keys():
            if feat_dict[feat] > 5:
                print(feat, file=f)


if __name__ == "__main__":
    with codecs.open('output\\train_tagging.txt', 'r', 'utf-8') as f:
        feature_extract(f, gather_feature)
    # save_features('output\\features.txt')
