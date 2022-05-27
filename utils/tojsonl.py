import jsonlines
import json
import argparse
import glob

from tqdm import tqdm

parser = argparse.ArgumentParser(description='Process data into jsonlines')
parser.add_argument('-d', '--data_dir', type=str, help='directory of data', default='data')
parser.add_argument('-o', '--output', type=str, help='output file', default='data.jsonl')
args = parser.parse_args()

print(f'Writing to {args.output}')

files = glob.glob(f'{args.data_dir}/*/*.txt')
with jsonlines.open(args.output, mode='w') as writer:
    for file in tqdm(files):
        with open(file, 'r', encoding='utf-8') as f:
            writer.write({'text': f.read()})

print('Done')
