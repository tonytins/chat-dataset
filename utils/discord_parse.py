import json
import argparse
import tqdm
import glob

from clean import clean

def format_channel(metadata):
    return f'[Name: #{metadata["name"]}; Description: {metadata["topic"]};]'

def worker_parse(filename, out_filename=None, **kwargs):
    data = json.load(open(filename, 'r', encoding='utf-8'))
    messages = data['messages']
    metadata = data['channel']

    msgs = []

    for message in tqdm.tqdm(messages):
        msg = ''
        if 'anonymous' in kwargs and kwargs['anonymous']:
            author = ''
        else:
            author = message['author']['name'] + ': '
        if message['embeds']:
            embed_content = ''
            if message['embeds'][0]['title']:
                embed_content = embed_content + f'Embed Title: {message["embeds"][0]["title"]};'
            if message['embeds'][0]['description']:
                desc = message['embeds'][0]['description']
                if desc[-1] == '.':
                    desc = desc[:-1]
                embed_content = embed_content + f' Embed Description: {desc};'
            msg = f'[{embed_content}]'
        if message['attachments']:
            if message['attachments'][0]['url'].endswith(('.png', '.jpeg', '.jpg')) and message['attachments'][0]['url'].startswith('http'):
                msg = '[Image attached]'
        if message['content']:
            msg = ''
        msgs.append(f'{author}{clean(message["content"])}{msg}')
    
    if out_filename == None:
        out_filename = filename.replace('.json', '.txt')
    with open(out_filename, 'w', encoding='utf-8') as f:
        f.write('⁂\n'+format_channel(metadata)+'\n⁂\n')
        f.write('\n'.join(msgs))
        
parser = argparse.ArgumentParser(description='Process Discord JSONs')
parser.add_argument('-f', '--file', type=str, help='file to process', required=False)
parser.add_argument('-a', '--anonymous', action='store_true', help='anonymous author')
parser.add_argument('-i', '--in_dir', type=str, help='directory to process', required=False)
parser.add_argument('-o', '--out_dir', type=str, help='directory to output', required=False)
args = parser.parse_args()

if __name__ == '__main__':
    if args.file:
        worker_parse(args.file, anonymous=args.anonymous)
    
    if args.in_dir and args.out_dir:
        files = glob.glob(args.in_dir+'/*.json')
        for file in files:
            try:
                worker_parse(file, out_filename=args.out_dir+'/'+file.split('/')[-1].replace('.json', '.txt'), anonymous=args.anonymous)
            except json.JSONDecodeError:
                print(f'JSON Validation error in "{file}", skipping.')
                continue