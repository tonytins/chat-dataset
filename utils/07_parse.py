from re import T
import parse
import argparse

from clean import clean

parser = argparse.ArgumentParser(description='Process some 07th stuff idk')
parser.add_argument('-f', '--file', type=str, help='file to process', required=True)
args = parser.parse_args()

with open(args.file, 'r') as f:
    lines = f.readlines()

jap_characters = ['。', '「', '」', '？', '！', '、', '…', 'ー']

author = parse.parse('\ufeff== {0} ==\n', lines[0])[0]

with open('output.txt', 'w') as f:
    for line in lines:
        if line.startswith('\ufeff'):
            continue
        # check if line has jap_characters
        if any(substr in line for substr in jap_characters):
            continue
        if line.startswith('\n==') or line.startswith('=='):
            try:
                author = parse.parse('== {0} ==\n', line)[0]
            except:
                author = 'Narrator'
            continue
        if line == '\n':
            continue
        line = line.rstrip()
        if author == 'Narrator':
            f.write(clean('[' + line.replace('\"', '').lstrip().rstrip() + ']').replace('\"', '')+'\n')
        else:
            txt = line.replace('\"', '')
            if '<Meta End>' in clean(txt) or '<Meta Start>' in clean(txt):
                continue
            f.write(clean(author + ': ' + line.replace('\"', '')).replace('\"', '')+'\n')

with open('output.txt', 'r') as f:
    lines = f.read()

def clean_07(txt):
    txt = txt.replace(']\n[', ' ')
    txt = txt.replace('[ ', '[')
    txt = txt.replace(' ]', ']')
    txt = txt.replace('\n\n', '\n')
    txt = txt.replace('~ib~', '**')
    txt = txt.replace('#fefefe', '')
    txt = txt.replace('<white>', '')
    txt = txt.replace('<red>', '')
    txt = txt.replace('<blue>', '')
    txt = txt.replace('<Meta End>', '')
    txt = txt.replace('<Meta Start>', '')
    return txt

with open('output.txt', 'w') as f:
    f.write(clean_07(lines))