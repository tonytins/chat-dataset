import os
import json
import tqdm
import re

from clean import clean

authors = {
    'Alice': 'Alice Margatroid',
    'Hourai': 'Hourai',
    'Shanghai': 'Shanghai',
    'Marisa': 'Marisa Kirisame',
    'Patchouli': 'Patchouli Knowledge',
    'Yuuka': 'Yuuka Kazami',
    'Cirno': 'Cirno',
    'Remilia': 'Remilia Scarlet',
    'Koakuma': 'Koakuma',
    'Medicine': 'Medicine Melancholy',
    'Shinki': 'Shinki',
    '???': '???',
    'Flandre': 'Flandre Scarlet',
    'Rumia': 'Rumia',
    'Meiling': 'Hong Meiling',
    'Sakuya': 'Sakuya Izayoi',
    'Reimu': 'Reimu Hakurei',
    'Yukari': 'Yukari Yakumo',
    'Chen': 'Chen',
    'Sanae': 'Sanae Kochiya',
    'Ran': 'Ran Yakumo',
    'Letty': 'Letty Whiterock',
    'Lyrica': 'Lyrica Prismriver',
    'Lunasa': 'Lunasa Prismriver',
    'Merlin': 'Merlin Prismriver',
    'Sisters': 'Lyrica, Lunasa, and Merlin',
    'Youmu': 'Youmu Konpaku',
    'Yuyuko': 'Yuyuko Saigyouji',
    'Marisa\nYuyuko': 'Marisa and Yuyuko',
    'Reimu\nYuyuko': 'Reimu and Yuyuko',
    'Sakuya\nYuyuko': 'Sakuya and Yuyuko',
    'Keine': 'Keine Kamishirasawa',
    'Kaguya': 'Kaguya Houraisan',
    'Mokou': 'Fujiwara no Mokou',
    'Wriggle': 'Wriggle Nightbug',
    'Mystia': 'Mystia Lorelei',
    'Reisen': 'Reisen Udongein Inaba',
    'Eirin': 'Eirin Yagokoro',
    '\xa0': '???',
    'Aya': 'Aya Shameimaru',
    'Tewi': 'Tewi Inaba',
    'Komachi': 'Komachi Onozuka',
    'Eiki': 'Eiki Shiki',
    'Kanako': 'Kanako Yasaka',
    'Suwako': 'Suwako Moriya',
    'Minoriko': 'Minoriko Aki',
    'Hina': 'Hina Kagiyama',
    'Nitori': 'Nitori Kawashiro',
    'Iku': 'Iku Nagae',
    'Tenshi': 'Tenshi Hinanawi',
    'Suika': 'Suika Ibuki',
    'Koishi': 'Koishi Komeiji',
    'Satori': 'Satori Komeiji',
    'Yamame': 'Yamame Kurodani',
    'Parsee': 'Parsee Mizuhashi',
    'Yuugi': 'Yuugi Hoshiguma',
    'Rin': 'Rin Kaenbyou',
    'Utsuho': 'Utsuho Reiuji',
    'Kogasa': 'Kogasa Tatara',
    'Nue': 'Nue Houjuu',
    'Nazrin': 'Nazrin',
    'Ichirin': 'Ichirin Kumoi',
    'Minamitsu': 'Minamitsu Murasa',
    'Shou': 'Shou Toramaru',
    'Byakuren': 'Byakuren Hijiri',
    'Master Big Catfish': 'Master Big Catfish',
    'Hatate': 'Hatate Himekaidou',
    'Luna': 'Luna Child',
    'Star': 'Star Sapphire',
    'Sunny': 'Sunny Milk',
    'Mamizou': 'Mamizou Futatsuiwa',
    'Kyouko': 'Kyouko Kasodani',
    'Yoshika': 'Yoshika Miyako',
    'Seiga': 'Seiga Kaku',
    'Futo': 'Mononobe no Futo',
    'Miko': 'Toyosatomimi no Miko',
    'Hijiri': 'Byakuren Hijiri',
    'Kokoro': 'Hata no Kokoro',
    '&lt;miko2&gt;': 'Toyosatomimi no Miko\'s Clone',
    'Benben': 'Benben Tsukumo',
    'Yatsuhashi': 'Yatsuhashi Tsukumo',
    'Raiko': 'Raiko Horikawa',
    'Wakasagihime': 'Wakasagihime',
    'Sekibanki': 'Sekibanki',
    'Kagerou': 'Kagerou Imaizumi',
    'Seija': 'Seija Kijin',
    'Shinmyoumaru': 'Shinmyoumaru',
    'Kasen': 'Kasen Ibaraki',
    'Usami': 'Sumireko Usami',
    'Doremy': 'Doremy Sweet',
    'Junko': 'Junko',
    'Hecatia': 'Hecatia Lapislazuli',
    'Seiran': 'Seiran',
    'Ringo': 'Ringo',
    'Sagume': 'Sagume Kishin',
    'Clownpiece': 'Clownpiece',
    'Udonge': 'Reisen Udongein Inaba',
    'Joon': 'Joon Yorigami',
    'Shion': 'Shion Yorigami',
    'Joon\nShion': 'Joon and Shion',
    'Usami2': 'Sumireko Usami\'s Clone',
    'Usami3': 'Sumireko Usami\'s Other Clone',
    'Shinmyoumaru2': 'Shinmyoumaru\'s Clone',
    'Mai': 'Mai',
    'Satono': 'Satono Nishida',
    'Okina': 'Okina Matara',
    'Eternity': 'Eternity Larva',
    'Nemuno': 'Nemuno Sakata',
    'Aunn': 'Aunn Komano',
    'Narumi': 'Narumi Yatadera',
    'Sumireko': 'Sumireko Usami',
    'Kutaka': 'Kutaka Niwatari',
    'Marisa(Wolf)': 'Marisa Kirisame',
    'Saki': 'Saki Kurokuma',
    'Eika': 'Eika Ebisu',
    'Urumi': 'Urumi Ushizaki',
    'Yachie': 'Yachie Kicchou',
    'Mayumi': 'Mayumi Joutouguu',
    'Keiki': 'Keiki Haniyasushin',
    'Marisa(Otter)': 'Marisa Kirisame',
    'Marisa(Eagle)': 'Marisa Kirisame',
    'Reimu(Wolf)': 'Reimu Hakurei',
    'Reimu(Otter)': 'Reimu Hakurei',
    'Reimu(Eagle)': 'Reimu Hakurei',
    'Youmu(Wolf)': 'Youmu Konpaku',
    'Youmu(Otter)': 'Youmu Konpaku',
    'Youmu(Eagle)': 'Youmu Konpaku',
    'Tsukasa': 'Tsukasa Kudamaki',
    'Momoyo': 'Momoyo Himemushi',
    'Misumaru': 'Misumaru Tamatsukuri',
    'Mike': 'Mike Goutokuji',
    'Takane': 'Takane Yamashiro',
    'Sannyo': 'Sannyo Komakusa',
    'Megumu': 'Megumu Iizunamaru',
    'Chimata': 'Chimata Tenkyuu',
}

# regex to remove strings like &lt;balloon$a11x3&gt;
exp = re.compile(r'&lt;.*?&gt;')

def worker_parse_hourai(filename, out_filename=None):
    # parse csv file
    messages = []

    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
        lines = data.split('\n')
        for line in lines:
            if line.startswith('name,line'):
                continue
            line = line.split(',')
            if len(line) < 2:
                continue
            author = line[0]
            text = clean(line[1].replace('\"', ''))
            messages.append(f'{authors[author]}: {text}')
    
    # write to file
    with open(out_filename, 'w', encoding='utf-8') as f:
        txt = '\n'.join(messages)
        f.write('⁂\n[Title: Hourai; Genre: Touhou Project]\n⁂\n')
        f.write(txt)
    
    return len(messages)

def worker_parse_dialogue(filename, out_filename=None):
    # open json
    messages = []
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for message in data:
            # first, check if author is in dict values
            author = message['Name']
            # iterate over values
            for key, value in authors.items():
                if value == author:
                    author = key
                    break
            author = authors[author]
            text = clean(message['Text']).replace('&#160;?"@', '').replace('&amp;', '').replace('&#160;', '').replace('\ ', '').replace('\. ', '\n')
            for key, value in authors.items():
                text = text.replace(key, value)
            text = exp.sub('', text)
            messages.append(f'{author}: {text}')
    
    # write to file
    with open(out_filename, 'w', encoding='utf-8') as f:
        txt = '\n'.join(messages)
        f.write('⁂\n[Title: The Touhou Project]\n⁂\n')
        f.write(txt.replace('\n\n', '\n'))
    
    return len(messages)

def dump_stats(length, name):
    stats = {'misc': {}}
    if os.path.exists('stats.json'):
        stats = json.load(open('stats.json', 'r', encoding='utf-8'))
    if 'misc' not in stats:
        stats['misc'] = {}
    stats['misc'][name] = length
    with open('stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f)

def parse():
    if not os.path.exists('./data/misc'):
        os.mkdir('./data/misc')
    dump_stats(worker_parse_hourai('./raw/misc/lines.csv', './data/misc/lines.txt'), 'hourai')
    dump_stats(worker_parse_dialogue('./raw/misc/dialogue.json', './data/misc/dialogue.txt'), 'dialogue')

if __name__ == '__main__':
    parse()