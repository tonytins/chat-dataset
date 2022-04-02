import os
import json

if __name__ == '__main__':
    # load stats.json
    stats = {}
    if os.path.exists('stats.json'):
        stats = json.load(open('stats.json', 'r', encoding='utf-8'))
    else:
        print('No stats.json found.')
        exit(1)

    print('-- Convo1 Dataset Stats --')
    print(f'Datasets Available: {len(stats)}')

    total_total = 0
    for dataset in stats.keys():
        total = 0
        print(f'\n-- Dataset Name: {dataset} --')
        for guild in sorted(stats[dataset].items(), key=lambda x: x[1], reverse=True):
            print(f'{guild[0]}: {guild[1]}')
            total += guild[1]
        print(f'\nTotal Messages in {dataset}: {total}\n')
        total_total += total
    
    print(f'\nTotal Messages in Convo Dataset: {total_total}\n')