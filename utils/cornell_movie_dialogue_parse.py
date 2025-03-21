# Parses the Cornell Movie Dialogue Corpus https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html
import os
import json
import argparse
import re
import tqdm

from clean import clean


class InvalidFormatError(Exception):
    pass


class InvalidLineError(Exception):
    pass


def format_name(name, raw_name):
    return name if raw_name else name[0].upper() + name[1:].lower()


# parses movie_lines.txt into a dictionary with the lineID as the key and the line as the value
def get_lines(filename, raw_name=False):
    lines = dict()
    with open(filename, 'r', encoding='windows-1252') as file:
        for row in tqdm.tqdm(file, desc='Reading lines'):
            row = row.split(' +++$+++ ')
            if len(row) != 5:
                raise InvalidFormatError(f'{filename} is not formatted correctly')

            lineID = row[0]
            name = row[3]
            line = row[4]

            # It seems that the dataset contains lines that aren't actually lines and have no name
            if len(name) == 0:
                lines[lineID] = None
                continue
            lines[lineID] = clean(format_name(name, raw_name) + ': ' + line)
    return lines


# parses movie_titles_metadata.txt into a dictionary with the movieID as the key and the value a dictionary
# with the title, year, rating, num_votes, and genres
def get_movie_metadata(filename):
    metadata = dict()
    with open(filename, 'r', encoding='windows-1252') as file:
        for row in tqdm.tqdm(file, desc='Reading movie metadata'):
            row = row.rstrip('\n').split( ' +++$+++ ')
            if len(row) != 6:
                raise InvalidFormatError(f'{filename} is not formatted correctly')
            movieID = row[0]
            metadata[movieID] = {'title': row[1], 'year': row[2], 'rating':row[3], 'num_votes': row[4], 'genres': row[5]}
    return metadata


def format_movie_metadata(metadata):
    return f'[Title: {metadata["title"]}; Genres: {metadata["genres"].replace("[", "").replace("]", "")}]'.replace('\'', '')


def construct_dialogue(lineIDs, lines):
    dialogue = []
    for lineID in lineIDs:
        if lines[lineID] is None:
            raise InvalidLineError()
        dialogue.append(lines[lineID])
    return '\n'.join(dialogue)

def dump_stats(length, movie_id):
    stats = {'Cornell Movie-Dialogue Corpus': {}}
    if os.path.exists('stats.json'):
        stats = json.load(open('stats.json', 'r', encoding='utf-8'))
        if 'Cornell Movie-Dialogue Corpus' not in stats:
            stats['Cornell Movie-Dialogue Corpus'] = {}
    stats['Cornell Movie-Dialogue Corpus'][str(movie_id)] = length
    with open('stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f)

# parses movie_conversations.txt and puts the results in out_filename
def parse_conversations(conversation_filename, out_dir, lines, movie_metadata, stats=True):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(conversation_filename, 'r', encoding='utf-8') as conversation_file:
        for row in tqdm.tqdm(conversation_file, desc='Constructing dialogue'):
            row = row.split(' +++$+++ ')
            if len(row) != 4:
                raise InvalidFormatError(f'{conversation_filename} is not formatted correctly')

            movieID = row[2]
            lineIDs = re.findall(r'\'(\w+)\'', row[3])
            try:
                dialogue = construct_dialogue(lineIDs, lines)
            except InvalidLineError:
                continue
            with open(f'{out_dir}/{movieID}.txt', 'w', encoding='utf-8') as out_file:
                out_file.write(f'⁂\n{format_movie_metadata(movie_metadata[movieID])}\n⁂\n')
                out_file.write(f'{dialogue}\n')
                if stats:
                    dump_stats(len(dialogue.split('\n')), movieID)

def parse(args = None):
    if args == None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--in_dir', default='./raw/cornell movie-dialogs corpus')
        parser.add_argument('--out_dir', default='./data/cornell movie-dialogs corpus')
        parser.add_argument('--raw_name', action='store_true', default=False)
        parser.add_argument('--stats', action='store_true', default=True)
        args = parser.parse_args()
    try:
        lines = get_lines(args.in_dir + '/movie_lines.txt', args.raw_name);
        movie_metadata = get_movie_metadata(args.in_dir + '/movie_titles_metadata.txt')
        parse_conversations(args.in_dir + '/movie_conversations.txt', args.out_dir, lines, movie_metadata)
    except (FileNotFoundError, InvalidFormatError) as e:
        print(e)
        exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Cornell Movie Dialogue Corpus', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--in_dir', type=str, help='directory to process', default='.')
    parser.add_argument('-o', '--out_file', type=str, help='file to output', default='cornell_movie_dialogue.txt')
    parser.add_argument('-r', '--raw_name', action='store_true', help='use speaker tags as they appear in the dataset instead of normalized names')
    parser.add_argument('-s', '--stats', action='store_true', help='store stats')
    args = parser.parse_args()
    parse(None)
