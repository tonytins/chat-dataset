import parse
import os
import json

from clean import clean

def dump_stats(s, index):
    stats = {}
    if os.path.exists('stats.json'):
        stats = json.load(open('stats.json', 'r', encoding='utf-8'))
    else:
        stats = {'visualnovels': {}}
    if 'visualnovels' not in stats:
        stats['visualnovels'] = {}
    stats['visualnovels'][f'Umineko no Naku Koro ni {str(index)}'] = s
    with open('stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f)

def worker_parse(filename, out_filename=None, stats=True, index=0):
    with open(filename, 'r') as f:
        lines = f.readlines()

    jap_characters = ['。', '「', '」', '？', '！', '、', '…', 'ー']

    author = parse.parse('\ufeff== {0} ==\n', lines[0])[0]

    with open(out_filename, 'w') as f:
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

    with open(out_filename, 'r') as f:
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

    with open(out_filename, 'w') as f:
        dump_stats(len(lines.split('\n')), index)
        description = "You have been given a chance to catch a glimpse of the family conference held annually by the Ushiromiya family. The remaining life in the old family head who has built up a vast fortune is very slim. To his children, the greatest point of contention at this family conference is the distribution of his inheritance. Everyone desires all that money, no one relents, and no one believes. Who will gain the old head's vast inheritance? Where is the 10 tons of gold that the old head is said to have hidden? Can the unnerving riddle of the epitaph which is said to point to the location of that gold be solved? In the midst of this, a suspicious letter is sent from one claiming to be a witch. The presence of a 19th person on this island, which should only have 18, begins to hang in the air. Brutal murders repeat, and unsolvable riddles are left at the scene. How many will die? How many will live? Or will everyone die? Is the culprit one of the 18, or not? Is the culprit a 'human', or a 'witch'? Please, enjoy this isolated island, western mansion, mystery-suspense gadget of the good old days to the fullest."
        metadata = '⁂\n' + f'[Title: Umineko no Naku Koro ni; Description: {description}]' + '\n⁂' + '\n'
        f.write(metadata)
        f.write(clean_07(lines))

if __name__ == '__main__':
    files = [
        './raw/visualnovel/ep1-4_EN__JP.txt',
        './raw/visualnovel/ep5-8_EN__JP.txt',
    ]

    output_files = [ i.replace('raw', 'data') for i in files ]
    
    for i in range(len(files)):
        worker_parse(files[i], output_files[i], stats=True, index=i)