#! /usr/bin/python
import argparse
from itertools import cycle, islice, izip_longest
import os
import re
import string
import sys

try:
	import colorama
except ImportError:
	if sys.platform.startswith("win"):
		print "Warning, you need colorama python module to display pretty"
		print "terminal output. Procede at your own risk"
else:
	colorama.init()

class bcolors(object):
	CIS = '\033['
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	@classmethod
	def format_string(cls, target, bright = False, background = False, color = 0, bold = False):
		#sanity check color to be in range [0, 7]
		if not (0 <= color <= 7):
			return None
		tmp = cls.CIS
		#dark colors are 30+i, light colors are 90+i
		#dark backgroands are 40+i, light backgrounds are 100+i
		base = 30
		if(bright):
			base += 60
		if(background):
			base += 10
		base += color
		#compose the opening qualifier
		tmp += str(base)
		if(bold):
			tmp += ';1'
		#close the qualifiers
		tmp += 'm'
		return tmp + target + cls.ENDC

class MonoSubstitution(object):
	def __init__(self):
		self.ciphertext = ''
		self.Ctext = [x for x in string.ascii_uppercase]
		self.Ptext = ['_' for x in range(0, len(string.ascii_uppercase))]
		self._CtP_mapping = {key: None for key in self.Ctext}
		#internal list of statistics used to generate frequency charts
		self._monograms = {'E': 529117365, 'T': 390965105, 'A': 374061888, 'O': 326627740, 
						   'I': 320410057, 'N': 313720540, 'S': 294300210, 'R': 277000841,
						   'H': 216768975, 'L': 183996130, 'D': 169330528, 'C': 138416451,
						   'U': 117295780, 'M': 110504544, 'F': 95422055, 'G': 91258980,
						   'P': 90376747, 'W': 79843664, 'Y': 75294515, 'B': 70195826, 
						   'V': 46337161, 'K': 35373464, 'J': 9613410, 'X': 8369915, 
						   'Z': 4975847, 'Q': 4550166, 'total': 4374127904}
		self.monogram_freq = {Y[0]: float(Y[1])/self._monograms['total'] for Y in self._monograms.items() if Y[0] is not 'total'} 
		#these are already sorted by frequency
		#generated by google word list of several trillion chars
		self._monographs_order = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'L',
								  'D', 'C', 'U', 'M', 'F', 'P', 'G', 'W', 'Y', 'B',
								  'V', 'K', 'X', 'J', 'Q', 'Z']
		self._digraphs_order = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN',
						 'ND', 'TI', 'ES', 'OR', 'TE', 'OF', 'ED', 'IS', 'IT',
						 'AL', 'AR', 'ST', 'TO', 'NT', 'NG', 'SE', 'HA', 'AS',
						 'OU', 'IO', 'LE', 'VE', 'CO', 'ME', 'DE', 'HI', 'RI',
						 'RO', 'IC', 'NE', 'EA', 'RA', 'CE', 'LI', 'CH', 'LL',
						 'BE', 'MA', 'SI', 'OM', 'UR']
		self._trigraphs_order = ['THE', 'AND', 'ING', 'ION', 'TIO', 'ENT', 'ATI', 'FOR',
						  'HER', 'TER', 'HAT', 'THA', 'ERE', 'ATE', 'HIS', 'CON',
						  'RES', 'VER', 'ALL', 'ONS', 'NCE', 'MEN', 'ITH', 'TED',
						  'ERS', 'PRO', 'THI', 'WIT', 'ARE', 'ESS', 'NOT', 'IVE',
						  'WAS', 'ECT', 'REA', 'COM', 'EVE', 'PER', 'INT', 'EST',
						  'STA', 'CTI', 'ICA', 'IST', 'EAR', 'AIN', 'ONE', 'OUR',
						  'ITI', 'RAT']
		self.ComputedFlag = False
		self._cipher_monographs = {}
		self._cipher_digraphs = {}
		self._cipher_trigraphs = {}

		self._cipher_monographs_order = []
		self._cipher_digraphs_order = []
		self._cipher_trigraphs_order = []

	def display_ciphertext(self, sub = False):
		#first get string of all characters unmapped and mapped
		is_mapped = set([x for x in self._monographs_order if self._CtP_mapping[x] is not None])
		not_mapped = set([x for x in self._monographs_order if self._CtP_mapping[x] is None])
		#sanity check that neither list should share elements
		if len(is_mapped.intersection(not_mapped)) != 0:
			#panic
			print "error, duplicated mapping characters"
			return False
		#easy route is just plain printin
		if sub == False:
			print self.ciphertext
		else:
			if len(self.ciphertext) == 0:
				print 
				return
			#now we have to parse things
			s_m = []
			s_un = []
			#check the first char to see if it is mapped or not
			#we will insert a dummy element if it is mapped so our
			#zipping of two lists will work correctly
			if self.ciphertext[0] in is_mapped:
				s_un.append('')
			#make a copy of the cipher text string
			str_cpy = self.ciphertext
			regex_is_mapped = re.compile('['+''.join(is_mapped)+']*')
			#unmapped will be everything that is not mapped
			regex_un_mapped = re.compile('[^'+''.join(is_mapped)+']*')

			unmapped_split = regex_un_mapped.split(str_cpy)
			#translate the tmporary array
			tmp_array = []
			for segment in unmapped_split:
				accum = ''
				for character in segment:
					if character in self._CtP_mapping:
						accum += self._CtP_mapping[character]
					else:
						accum += character
				tmp_array.append(accum)
			#colorize all of the mapped values
			s_m += [bcolors.format_string(x, bright = True, background = True, color = 2) for x in tmp_array]
			s_un = regex_is_mapped.split(str_cpy)
			output_line = ''

			for x in izip_longest(s_un, s_m, fillvalue = '--'):
				output_line += x[0]
				output_line += x[1]
			
			print output_line

	def clear_ciphertext(self):
		self.ciphertext = ''
		self.ComputedFlag = False
		self._cipher_monographs = {}
		self._cipher_digraphs = {}
		self._cipher_trigraphs = {}

		self._cipher_monographs_order = []
		self._cipher_digraphs_order = []
		self._cipher_trigraphs_order = []

	def compute_frequency(self, force = False):
		#no need to do extra work if we already computed the graphs
		if self.ComputedFlag and not force:
			return None
		#compute the graphs
		regex_valid_chars = re.compile('[^'+''.join(self.Ctext)+']*')
		#only bother with the valid chars
		valid_chars = regex_valid_chars.sub('', self.ciphertext)
		total_length = len(valid_chars)
		for index, character in enumerate(valid_chars):
			if character in self._CtP_mapping:
				#monograph
				if character in self._cipher_monographs:
					self._cipher_monographs[character] += 1
				else:
					self._cipher_monographs[character] = 1

				#digraph
				if index < total_length-1:
					token = ''
					token = character + valid_chars[index+1]
					if token in self._cipher_digraphs:
						self._cipher_digraphs[token] += 1
					else:
						self._cipher_digraphs[token] = 1
				#trigraph
				if index < total_length-2:
					token = ''
					token = character + valid_chars[index+1] + valid_chars[index+2]
					if token in self._cipher_trigraphs:
						self._cipher_trigraphs[token] += 1
					else:
						self._cipher_trigraphs[token] = 1


		#now create the ordered list by frequency
		tmp_array = [x for x in self._cipher_monographs.items()]
		self._cipher_monographs_order = [x[0] for x in sorted(tmp_array, key=lambda item: item[1], reverse = True)]
		del tmp_array

		tmp_array = [x for x in self._cipher_digraphs.items()]
		long_array = sorted(tmp_array, key=lambda item: item[1], reverse = True)
		#shorten the digraphs and trigraphs to length 50
		self._cipher_digraphs_order = [x[0] for x in long_array[0:min(len(long_array), 50)]]
		del tmp_array
		del long_array
		tmp_array = [x for x in self._cipher_trigraphs.items()]
		long_array = sorted(tmp_array, key = lambda item: item[1], reverse = True)
		self._cipher_trigraphs_order = [x[0] for x in long_array[0:min(len(long_array), 50)]]

		self.ComputedFlag = True
		return None

	def add_rule(self, cipher, plain):
		#make sure subsitutions can be one to one
		if(len(cipher) != len(plain)):
			return None
		for index,character in enumerate(cipher):
			#make sure character is a letter
			if character in string.ascii_letters:
				character = character.upper()
				self.Ptext[self.Ctext.index(character)] = plain[index].upper()
				if plain[index] == '_':
					self._CtP_mapping[character] = None
				else:
					self._CtP_mapping[character] = plain[index].upper()
			else:
				#we must have a valid cipher text character to map to plaintext
				return None

	def __repr__(self):
		return "Mappings:\nC: "+" ".join(self.Ctext)+'\nP: '+" ".join(self.Ptext)

	def show_ngrams(self, ngram = -1, subs = False):
		#if it is zero then we will do all of them
		if ngram == -1:
			headers = ["Monographs", "Digraphs", "Trigraphs"]
			ngram_ordered = [self._cipher_monographs_order, self._cipher_digraphs_order, self._cipher_trigraphs_order]
			ngram_counter = [self._cipher_monographs, self._cipher_digraphs, self._cipher_trigraphs]
			english_ngrams = [self._monographs_order, self._digraphs_order, self._trigraphs_order]
		elif ngram == 1:
			headers = ["Monographs"]
			ngram_ordered = [self._cipher_monographs_order]
			ngram_counter = [self._cipher_monographs]
			english_ngrams = [self._monographs_order]
		elif ngram == 2:
			headers = ["Digraphs"]
			ngram_ordered = [self._cipher_digraphs_order]
			ngram_counter = [self._cipher_digraphs]
			english_ngrams = [self._digraphs_order]
		elif ngram == 3:
			headers = ["Trigraphs"]
			ngram_ordered = [self._cipher_trigraphs_order]
			ngram_counter = [self._cipher_trigraphs]
			english_ngrams = [self._trigraphs_order]
		else:
			#that option was not valid
			return False
		#use array to vist each of them
		for overt_index, ordering in enumerate(ngram_ordered):
			tmp_ngram = ordering
			tmp_counter = ngram_counter[overt_index]
			print headers[overt_index]
			#copy the counts because after we colorize the output we can
			#no longer use them as keys to look up the counts
			tmp_ngram_count = [tmp_counter[x] for x in tmp_ngram]
			#if subs then we substitute the characters we know about
			#and form a new list for latter formatting and printing
			if(subs):
				tmp_ngram = []
				#colorize each digraph and translate it at same time
				for element in ordering:
					tmp_elm = ''
					#check each character
					for character in element:
						#ignore characters not in mapping
						if (character in self._CtP_mapping) and (self._CtP_mapping[character] is not None):
							tmp_elm += bcolors.format_string(self._CtP_mapping[character],
											background = True, bright = True, color = 2)
						else:
							tmp_elm += character
					tmp_ngram.append(tmp_elm)

			#now print out the digraphs
			for index,element in enumerate(tmp_ngram):
				sys.stdout.write(element + ' ')
				sys.stdout.write(str(tmp_counter[ordering[index]]))

				if(index < len(ordering)):
					sys.stdout.write(' ' + english_ngrams[overt_index][index])
				else:
					sys.stdout.write('  ')
				#now write the cipher text digraph count
				sys.stdout.write('\n')

def main():
	parser = argparse.ArgumentParser(prog = "Mono Subsitution Helper", 
	description = "assists in decoding a mono substitution cipher")
	#parser.add_argument('cmd', choices = ['create','delete','help','quit'])
	parser.add_argument('-decode', nargs = 2, 
			help = "<A> <B> where A in ciphertext maps to B in plaintext",
			metavar = '<char>')
	parser.add_argument('-q', '--quit', action = 'store_true', default = False, 
			help = "Exit the program, discarding all data")
	parser.add_argument('--load-file', nargs = 1, metavar = "<filename>", default = False,
			help = "Loads a file and treats it as cipher text")
	parser.add_argument('--load-string', nargs = 1, metavar = "<string>", default = False,
			help = "Loads a string of cipher text from command line")
	parser.add_argument('--sub', action = 'store_true', default = False,
			help = "Substitute the characters in the ciphetext with their assigned mappings")
	parser.add_argument('--to-upper', action = 'store_true', default = False,
		 	help = "Changes lowercase ASCII characters in input format to upper case")
	parser.add_argument('--show-mapping', action = 'store_true', default = False,
			help = "show the individual character level mapping of the cipher")
	parser.add_argument('-c', '--ciphertext', action = 'store_true' ,default = False,
			help = "print the cipher text to the screen" )
	parser.add_argument('-f', '--frequency', nargs = '?', default = False, const = [0],
			help = "compute a frequency analysis on ciphertext, default behaviour \
			is to print counts for the 1-grams 2-grams and 3-grams in the ciphertext \
			sorted from most frequent to least frequent shown alongside sorted frequency \
			of n-grams for english language \
			Use optional argument of [1,2,3] to only show a specific n-gram frequency \
			analysis, any other values will be ignored", metavar = "1,2,3")

	subs = MonoSubstitution();
	while True:
		astr = raw_input('$ ')
		# print astr
		try:
			args = parser.parse_args(astr.split())
		except SystemExit:
			# trap argparse error message
			#print 'error'
			continue

		if args.quit:
			break
		if args.decode:
			subs.add_rule(args.decode[0], args.decode[1])
			continue
		if args.load_file:
			filename = os.path.join(os.getcwd(),args.load_file[0])
			#check the filesize since the designed behaviour is to
			#load the entire ciphertext into memory and make several copies
			try:
				statinfo = os.stat(filename)
			except OSError:
				print "{} does not exist".format(filename)
				continue
			#100 megabytes is maximum file size
			if(statinfo.st_size < 1024*1024*1024*100):
				#flush the old cipher text and remove all token counts from old data
				subs.clear_ciphertext()
				with open(filename, "r") as f:
					for line in f:
						#we have the option to force everything to upper case
						if args.to_upper:
							line = line.upper()
						subs.ciphertext += line
				
			else:
				print "File is too large"
		elif args.load_string:
			subs.clear_ciphertext()
			if args.to_upper:
				subs.ciphertext += args.load_string[0].upper()
			else:
				subs.ciphertext += args.load_string[0]
			print subs.ciphertext

		if args.show_mapping:
			print subs

		elif args.ciphertext:
			if args.sub:
				subs.display_ciphertext(True)
			else:
				subs.display_ciphertext(False)

		elif args.frequency:
			subs.compute_frequency()
			if args.sub:
				sub_flag = True
			else:
				sub_flag = False
			#show the frequency counts with 
			if args.frequency[0] == '1':
				subs.show_ngrams(ngram = 1, subs = sub_flag)
			elif args.frequency[0] == '2':
				subs.show_ngrams(ngram = 2, subs = sub_flag)
			elif args.frequency[0] == '3':
				subs.show_ngrams(ngram = 3, subs = sub_flag)
			else:
				#show mono, di, and trigraphs
				subs.show_ngrams(ngram = -1, subs = sub_flag)

if __name__ == '__main__':
	main()
