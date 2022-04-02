import random
import glob
import os
import json

import argparse

from tqdm import tqdm

import umi_parse
import cornell_movie_dialogue_parse
import eratoho_parse
import valhalla_parse
import discord_parse

def compile_raw():
    print('-- Parsing Umineko Data --\n')
    umi_parse.parse()
    print('\n-- Parsing Cornell Movie Dialogue Data --\n')
    cornell_movie_dialogue_parse.parse()
    print('\n-- Parsing Eratoho Data --\n')
    eratoho_parse.parse()
    print('\n-- Parsing Valhalla Data --\n')
    valhalla_parse.parse()
    print('\n-- Parsing Discord Data --\n')
    discord_parse.parse()

def compile_mtf_jax():
    # compiles dataset into a single text file to be tokenized by the mtf jax repo
    
    # get all the files with *.txt in ./data.
    files = glob.glob('data/*/*.txt')
    with open('output.txt', 'w', encoding='utf-8') as f:
        for file in tqdm(files):
            with open(file, 'r', encoding='utf-8') as f2:
                f.write(f2.read().replace('\n\n', '\n'))
                f.write('\n')
    
    # remove all double newlines
    lines = ''
    with open('output.txt', 'r', encoding='utf-8') as f:
        lines = f.read().replace('\n\n', '\n')
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(lines)

def compile_gpt_neo():
    # compile each file into a json lines file
    files = glob.glob('data/*/*.txt')
    # shuffle the files
    random.shuffle(files)
    with open('output.jsonl', 'w', encoding='utf-8') as f:
        for file in tqdm(files):
            with open(file, 'r', encoding='utf-8') as f2:
                f.write(json.dumps({'text': f2.read().replace('\n\n', '\n')}))
                f.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process raw data')
    parser.add_argument('-d', '--dont_compile', action='store_true', help='dont compile raw data', default=False)
    parser.add_argument('-m', '--mtf_jax', action='store_true', help='compile raw data into a single text file to be tokenized by the mtf jax repo')
    parser.add_argument('-g', '--gpt_neo', action='store_true', help='compile raw data into a single json lines file')
    args = parser.parse_args()

    if not args.dont_compile:
        compile_raw()
    if args.mtf_jax:
        compile_mtf_jax()
    if args.gpt_neo:
        compile_gpt_neo()

    print('Done!')
