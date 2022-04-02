import os
import json
import argparse
import tqdm
import glob

from clean import clean

def format_channel(metadata):
    return f'[Name: #{metadata["name"]}; Description: {metadata["topic"]}; Guild: {metadata["guild"]}]'

def worker_parse(filename, out_filename=None, **kwargs):
    data = json.load(open(filename, 'r', encoding='utf-8'))
    messages = data['messages']
    metadata = data['channel']
    metadata['guild'] = data['guild']['name']

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
    
    return (metadata, len(msgs))

def worker_dl(channel_id_path, auth_token):
    # channel_id_path is a json
    channel_id_data = json.load(open(channel_id_path, 'r', encoding='utf-8'))
    channel_ids = []
    print('Loading channel ids\nYou need to be in the following guilds to construct the dataset.\n')
    for guild in channel_id_data['guilds']:
        print(f'[Guild: {guild["name"]}; Invite: {guild["invite"]};]')
        for channel in guild['channels']:
            channel_ids.append(str(channel))
    print(f'\nTotal channels: {len(channel_ids)}\nTotal guilds: {len(channel_id_data["guilds"])}\n')
    print('Downloading messages...')
    channel_ids = ' '.join(channel_ids)
    os.system(f'discord-chat-exporter-cli export -t {auth_token} -f Json -c {channel_ids}')
    print('Moving files...')
    if not os.path.exists('raw/discord/'):
        os.mkdir('raw/discord/')
    for filename in glob.glob('*.json'):
        os.rename(filename, f'raw/discord/{filename}')

def dump_stats(s):
    stats = {}
    if os.path.exists('stats.json'):
        stats = json.load(open('stats.json', 'r', encoding='utf-8'))
        if 'discord' not in stats:
            stats['discord'] = {}
    else:
        stats = {'discord': {}}
    stats['discord'][s[0]['guild']+' - '+s[0]['name']] = s[1]
    with open('stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f)

def parse(args=None):
    parser = argparse.ArgumentParser(description='Process Discord JSONs')
    parser.add_argument('-f', '--file', type=str, help='file to process', required=False)
    parser.add_argument('-a', '--anonymous', action='store_true', help='anonymous author')
    parser.add_argument('-i', '--in_dir', type=str, help='directory to process', required=False, default='./raw/discord')
    parser.add_argument('-o', '--out_dir', type=str, help='directory to output', required=False, default='./data/discord')
    parser.add_argument('-d', '--dl', type=str, help='json file containing channel IDs to download', required=False)
    parser.add_argument('-t', '--token', type=str, help='discord auth token', required=False)
    parser.add_argument('-s', '--stats', action='store_true', help='write to stats', default=True)
    args = parser.parse_args()

    if args.dl:
        if not args.token:
            print('Please provide a Discord auth token')
            exit(1)
        worker_dl(args.dl, args.token)
        exit()
    if args.file:
        s = worker_parse(args.file, anonymous=args.anonymous)
        if args.stats:
            dump_stats(s)
        exit()
    if args.in_dir and args.out_dir:
        if not os.path.exists(args.out_dir):
            os.mkdir(args.out_dir)
        files = glob.glob(args.in_dir+'/*.json')
        for file in files:
            try:
                s = worker_parse(file, out_filename=args.out_dir+'/'+file.split('/')[-1].replace('.json', '.txt'), anonymous=args.anonymous)
                if args.stats:
                    dump_stats(s)
            except json.JSONDecodeError:
                print(f'JSON Validation error in "{file}", skipping.')
                continue

if __name__ == '__main__':
    parse()
