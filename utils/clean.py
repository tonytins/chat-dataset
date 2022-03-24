import re, io

# Character normalization

normalize_chars = {}
alphabets = io.open('utils/latin-alphabets.txt', mode='r', encoding='utf-8').read().strip().split('\n')

for alphabet in alphabets[1:]:
    for ind, char in enumerate(alphabet):
        try:
            normalize_chars[char] = alphabets[0][ind]
        except IndexError:
            print(alphabet, len(alphabet))
            break
normalize_chars.update({
    i:i for i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
})
normal_map = str.maketrans(normalize_chars)
del normalize_chars

# Regex patterns

r_space_cleaner = re.compile(r'\s+')
r_space_normalizer = re.compile(r'[\U00003000\U0000205F\U0000202F\U0000200A\U00002000-\U00002009\U00001680\U000000A0\t]+| {2,}')
r_newline_cleaner = re.compile(r'\n+')
r_single_apostrophe_normalizer = re.compile(r'[’]')
r_double_apostrophe_normalizer = re.compile(r'[“”]')
r_strange_apostrophe_normalizer = re.compile(r'[『』]')
r_url_cleaner = re.compile(r'^https?:\/\/.*[\r\n]*')

def clean(text):
    text = text.translate(normal_map)
    text = r_space_cleaner.sub(' ', text)
    #text = r_space_normalizer.sub(' ', text)
    text = r_newline_cleaner.sub(' ', text)
    text = r_single_apostrophe_normalizer.sub('\'', text)
    text = r_double_apostrophe_normalizer.sub('\"', text)
    text = r_strange_apostrophe_normalizer.sub('\"', text)
    text = r_url_cleaner.sub('[File URL attached]', text)
    return text
