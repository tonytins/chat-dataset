# Parses dialogue from the show Friends provided by the Character Mining project
# https://github.com/emorynlp/character-mining
# The tsv file can be downloaded with
# wget https://raw.githubusercontent.com/gmihaila/character-mining/developer/tsv/friends_transcripts.tsv
import argparse
import csv
import re
import tqdm

from clean import clean


class InvalidFormatError(Exception):
    pass


class InvalidUtteranceError(Exception):
    pass


def valid_csv(dict_reader):
    return (dict_reader.fieldnames is not None and
            set(dict_reader.fieldnames) == {'season_id', 'episode_id', 'scene_id', 'utterance_id', 'speaker', 'tokens', 'transcript'})


def format_conversation_metadata(utterance):
    return f'[Season: {utterance["season_id"]}; Episode: {utterance["episode_id"]}; Conversation: {utterance["scene_id"]};]'


def format_utterance(utterance):
    speaker = utterance['speaker']
    # there are some invalid lines with the speaker "unknown"
    if speaker == 'unknown':
        raise InvalidUtteranceError()
    # remove parenthetical description of characters
    speaker = re.sub(r'\(.*\)', '', speaker)
    speaker = speaker.strip()

    line = clean(utterance['transcript'])
    # there are some invalid empty lines
    if line == '':
        raise InvalidUtteranceError()

    return f'{speaker}: {line}'


def different_conversations(utterance1, utterance2):
    return (utterance1['season_id'] != utterance2['season_id'] or
            utterance1['episode_id'] != utterance2['episode_id'] or
            utterance1['scene_id'] != utterance2['scene_id'])


def parse_dialogue(in_filename, out_filename):
    with open(in_filename, 'r', encoding='utf-8') as in_file, open(out_filename, 'w', encoding='utf-8') as out_file:
        reader = csv.DictReader(in_file, delimiter='\t')
        if not valid_csv(reader):
            raise InvalidFormatError(f'{in_filename} is not formatted correctly')
        last_utterance = None
        for utterance in tqdm.tqdm(reader):
            if last_utterance is None or different_conversations(last_utterance, utterance):
                out_file.write(f'⁂\n{format_conversation_metadata(utterance)}\n⁂\n')
            try:
                out_file.write(f'{format_utterance(utterance)}\n')
            except InvalidUtteranceError:
                pass
            last_utterance = utterance


parser = argparse.ArgumentParser(description='Process Friends dialogue\n\n'
                                             'The data is taken from\n'
                                             'https://github.com/emorynlp/character-mining\n\n'
                                             'It can be downloaded with\n'
                                             'wget https://raw.githubusercontent.com/emorynlp/character-mining/master/tsv/friends_transcripts.tsv',
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('file', type=str, help='tsv file to process')
parser.add_argument('-o', '--out', type=str, help='file to output', default='friends_dialogue.txt')
args = parser.parse_args()

if __name__ == '__main__':
    try:
        parse_dialogue(args.file, args.out)
    except (FileNotFoundError, InvalidFormatError) as e:
        print(e)
        exit(1)
