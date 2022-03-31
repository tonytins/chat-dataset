import os
import json
import argparse
import tqdm
import glob
import re

from clean import clean

def format_channel(metadata):
	return f'[Name: #{metadata["name"]}; Description: {metadata["topic"]}; Guild: {metadata["guild"]}]'

def worker_parse(filename, out_filename=None, **kwargs):
	filtered_lines = []
	with open(filename, 'r', encoding='utf-8') as f:
		# data isnt json
		data = f.read()
		# iterate over lines
		for line in data.split('\n'):
			# remove left whitespace
			line = line.lstrip()
			# if line starts with ; then continue
			if line.startswith(';'):
				continue # semicolon lines are comments
			dialog_starters = ['PRINTFORML ', 'PRINT ', 'PRINTL ', 'PRINTFORMW', 'PRINTW', 'PRINTFORMDL']
			# inline for loop to see if line starts with dialog_starters
			if any(line.startswith(dialog_starter) for dialog_starter in dialog_starters):
				# remove dialog starters from line with for inline loop
				for dialog_starter in dialog_starters:
					if line.startswith(dialog_starter):
						line = line.replace(dialog_starter, '').lstrip().rstrip()
						break
				line = re.sub(r'\([^)]*\)', '', line)
				line = line.replace('%HIM_HER%', 'her')
				line = line.replace('%HE_SHE%', 'she')
				line = line.replace('%HIS_HER%', 'her')
				line = line.replace('%HIMSELF_HERSELF%', 'herself')
				line = line.replace('%CALLNAME:MASTER%', 'Master')
				line = line.replace('%CALLNAME:TARGET%', kwargs['character'])
				line = line.replace('%UNICODE%', '')
				line = line.replace('%PARSE%', 'Master')
				line = line.replace('%DISHNAME_TR%', 'food')
				line = line.replace('%" "%', '')
				line = line.replace('%TINKO%', 'member')
				line = line.replace('%HIP_TR%', 'hips')
				line = line.replace('%SEMEN%', 'cum')
				line = line.replace('%OPPAI_DESCRIPTION_TR%', 'voluptuous breasts')
				line = line.replace('%PANTSNAME%', 'skirt')
				line = line.replace('%UNDER_SKIRT_DESCRIPTION_TR%', 'lacy panties')
				line = line.replace('%SAMEN_DESCRIPTION%', 'hot liquid cum')
				line = line.replace('%SPLIT_G%', 'Master')
				line = line.replace('%SLIT%', 'slit')
				line = line.replace('%LOCALS%', '')
				line = line.replace('%CALLNAME:ARG%', 'your partner')
				line = line.replace('%CALLNAME:%', 'your partner')
				line = line.replace('%CAPITALIZE)%', 'Master')
				# remove text between \@ and #
				line = re.sub(r'\\@[^#]*#', '', line).lstrip().replace("\\@", "").replace("  ", " ")
				if line.startswith('「') or line.endswith('」'):
					line = line.replace("「", "").replace("」", "").lstrip()
					if line != "":
						filtered_lines.append(f'{kwargs["character"]}: {line}')
				else:
					if line != "":
						filtered_lines.append(f'[{line}]')
					
	with open(out_filename, 'w', encoding='utf-8') as f:
		f.write(f'⁂\n[Title: eratohoTW; Description: {kwargs["character"]} dialog {kwargs["index"]}]\n⁂\n')
		f.write('\n'.join(filtered_lines))
	
	return len(filtered_lines)
					

def dump_stats(length, character, index):
	stats = {}
	if os.path.exists('stats.json'):
		stats = json.load(open('stats.json', 'r', encoding='utf-8'))
	else:
		stats = {'eratoho': {}}
	stats['eratoho'][str(character)+' - '+str(index)] = length
	with open('stats.json', 'w', encoding='utf-8') as f:
		json.dump(stats, f)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process Discord JSONs')
	parser.add_argument('-i', '--in_dir', type=str, help='directory to process', required=False, default='./raw/eratoho')
	parser.add_argument('-o', '--out_dir', type=str, help='directory to output', required=False, default='./data/eratoho')
	parser.add_argument('-s', '--stats', action='store_true', help='write to stats', default=True)
	args = parser.parse_args()

	names = {
		'patchouli': 'Patchouli Knowledge',
		'ruukoto': 'Ruukoto',
		'youmu': 'Youmu Konpaku',
		'meiling': 'Hong Meiling',
		'mima': 'Mima',
		'kagerou': 'Kagerou Imaizumi',
		'yuuka': 'Yuuka Kazami',
		'kosuzu': 'Kosuzu Motoori',
		'akyuu': 'Akyuu Hieda',
		'shinmyoumaru': 'Sukuna Shinmyoumaru',
		'clownpiece': 'Clownpiece'
	}

	print('wat')

	if args.in_dir and args.out_dir:
		if not os.path.exists(args.out_dir):
			os.mkdir(args.out_dir)
		files = glob.glob(args.in_dir+'/*.ERB')
		for file in files:
			lines = worker_parse(file, out_filename=args.out_dir+'/'+file.split('/')[-1].replace('.ERB', '.txt'), character=names[file.split('/')[-1].split('_')[0]], index=int(file.split('/')[-1].split('_')[1].split('.')[0]))
			if args.stats:
				dump_stats(lines, names[file.split('/')[-1].split('_')[0]].split('.')[0], file.split('/')[-1].split('_')[1].split('.')[0])