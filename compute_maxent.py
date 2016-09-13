import codecs
import sys
from nltk.classify import MaxentClassifier


def load_data(filename):
    train = []
    for line in open(filename, mode='r'):
        sample = line.strip().split("_")
        y = sample[4]
        reason1 = {'-2': sample[0], '-1': sample[1], '1': sample[2], '2': sample[3]}
        if y == 'B':
            train.append((reason1, 'B'))
        elif y == 'S':
            train.append((reason1, 'S'))
        elif y == 'E':
            train.append((reason1, 'E'))
        else:
            train.append((reason1, 'M'))
    return train


def print_maxent_test_header():
    print(' ' * 11 + ''.join(['      test[%s]  ' % i
                              for i in range(len(test))]))
    print(' ' * 11 + '     p(B)  p(E) p(M) p(S)' * len(test))
    print('-' * (11 + 15 * len(test)))


def max_label(param, param1, param2, param3):
    pa = [param, param1, param2, param3]
    label = ['B', 'E', 'M', 'S']
    cm1 = 0
    cm2 = 2
    if pa[0] < param1:
        cm1 = 1
    if pa[2] < param3:
        cm2 = 3
    if pa[cm1] > pa[cm2]:
        return label[cm1]
    else:
        return label[cm2]


def test_maxent(algorithm, test, train):
    label = []
    print('%11s' % algorithm, end=' ')
    try:
        classifier = MaxentClassifier.train(
                train, algorithm, trace=0, max_iter=10)
    except Exception as e:
        print('Error: %r' % e)
        return

    for featureset in test:
        pdist = classifier.prob_classify(featureset)
        classifier.weights()
        label.append(max_label(pdist.prob('B'), pdist.prob('E'), pdist.prob('M'), pdist.prob('S')))

    return label


def save_label(label):
    filename1 = 'output/pos_tagging.txt'
    filename2 = 'output/test_tagging.txt'
    save_file = codecs.open(filename1, 'w', 'utf-8')
    read_file = codecs.open(filename2, 'r', 'utf-8')
    cnt = 0
    for s in read_file:
        words = s.split()
        if len(words) == 0:
            continue
        label_str = ""
        for x in words:
            label_str += x+'/'+label[cnt]+' '
            cnt += 1
        print(label_str, file=save_file)
    save_file.close()
    read_file.close()


def test_feature(words, i):
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


def generate_test(file):
    test_features = []
    for s in file:
        words = s.split()
        if len(words) == 0:
            continue
        # print(sent)
        l = len(words)
        for i in range(l):
            c = test_feature(words, i).split('_')
            test_features.append({'-2': c[0], '-1': c[1], '1': c[2], '2': c[3]})
    return test_features


if __name__ == '__main__':
    load_data('output\context.txt')
    file_test = codecs.open('output\\test_tagging.txt', 'r', 'utf-8')
    test = generate_test(file_test)
    print_maxent_test_header()
    label = test_maxent('IIS')
    save_label(label)
    sys.exit(0)
