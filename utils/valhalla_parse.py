import json
import os

from clean import clean

def dump_stats(s, day):
    stats = {}
    if os.path.exists('stats.json'):
        stats = json.load(open('stats.json', 'r', encoding='utf-8'))
    else:
        stats = {'visualnovels': {}}
    if 'visualnovels' not in stats:
        stats['visualnovels'] = {}
    stats['visualnovels'][f'VA-11 HALL-A {str(day)}'] = s
    with open('stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f)

def worker_parse(filename, out_filename, stats=True):
    data = json.load(open(filename, 'r', encoding='utf-8'))
    for day in range(len(data)):
        msgs = ['⁂', f'[Title: VA-11 HALL-A; Description: Day {day}]', '⁂']
        for entry in data[day]:
            if entry['type'] == 'dialogue':
                msgs.append(f'{entry["character"]}: {clean(entry["text"])}')
                msgs[-1] = msgs[-1].replace('  ', ' ').replace('\n', '')
        # split filename to include day number
        outfname = '.' + out_filename.split('.')[1] + f'_{day}.txt'
        with open(outfname, 'w', encoding='utf-8') as out_file:
            out_file.write('\n'.join(msgs))
        if stats:
            dump_stats(len(msgs), day)


if __name__ == '__main__':
    worker_parse('./raw/visualnovel/valhalla.txt', './data/visualnovel/valhalla.txt')