from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer
from posting import Posting
import json
from pathlib import Path
import re
from string import punctuation

def start(inverted_index):
	inverted_index = indexer(inverted_index)
	write_report(inverted_index)
	create_index_squared("inverted_index.txt")
	# print(indexer(inverted_index))


# https://stackoverflow.com/questions/39909655/listing-of-all-files-in-directory
def indexer(inverted_index):
	n = 0

	#/home/fghiasi/M1_project/searchEngine/examples/aiclub_ics_uci_edu
	#/home/fghiasi/inf141Proj2_last_update/inf141Proj2/Assignment3/DEV
	#documents = searching_all_files('/home/fghiasi/M1_project/searchEngine/examples/aiclub_ics_uci_edu')
	documents = ['C:\\Users\\NoobMaster69\\Desktop\\School\\CS 121 - Info Retrieval\\Assignments\\3-Search-Engine\\searchEngine\\examples\\aiclub_ics_uci_edu']
	for document in documents:
		n += 1
		content = extract_json_content(document)
		text = tokonize(content)
		word_freq = computeWordFrequencies(text)

		for i, token in enumerate(text):
			if token not in inverted_index:
				inverted_index[token] = []
			inverted_index[token].append(Posting(n, word_freq[token], i))
			# print(token, " ", Posting(n, word_freq[token], i))

	return inverted_index

def extract_json_content(path):
	file = None
	# https://stackoverflow.com/questions/713794/catching-an-exception-while-using-a-python-with-statement
	try:
		with open(path) as f:
			file = json.load(f)
	except EnvironmentError as error:
		print(error, " while reading ", path)
	if file:
		return file['content']

def create_index_squared(inverted_index_file):
	postingsSize = 0
	index_list = []

	with open(inverted_index_file) as f:
		start = 0
		for line in f:
			if "," not in line and '$' not in line:
				#line is token, not posting because of the comma
				#line is token, 0 is starting position
				index_list.append(line.strip('\n'))
			postingsSize += len(line) + 1
			if line.startswith('$'):
				index_list.append(start)
				start = postingsSize

	tmt_list = []
	for i in range(0, len(index_list), 2):
		tmt_list.append((index_list[i], index_list[i+1]))


	file = open("index_of_index.txt", "w")
	for tuple_item in sorted(tmt_list):
		string1 = "{} {}\n".format(tuple_item[0], tuple_item[1])
		file.write(string1)
	file.close()

# Tokens: all alphanumeric sequences in the dataset.
def tokonize(html_content):
	soup = BeautifulSoup(html_content, features='html.parser')
	stemmer = SnowballStemmer(language='english')
	# shelly -> shelli (result of snowball stemmer)
	# https://snowballstem.org/demo.html
	text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
	text_divs = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))

	tokens = list()
	for paragraph in text_p:
		for raw_word in paragraph.split():
			token = raw_word.strip(punctuation).lower()
			if token.isalnum():
				word = stemmer.stem(token)
				tokens.append(word)

	for paragraph in text_divs:
		for raw_word in paragraph.split():
			token = raw_word.strip(punctuation).lower()
			if token.isalnum():
				word = stemmer.stem(token)
				tokens.append(word)
	return tokens

def computeWordFrequencies(tokens):
	wordfreq = dict()
	for token in tokens:
		if token not in wordfreq:
			wordfreq[token] = 1
		else:
			wordfreq[token] += 1
	return wordfreq

def searching_all_files(directory):
	dirpath = Path(directory)
	assert(dirpath.is_dir())
	file_list = []
	for x in dirpath.iterdir():
		if x.is_file():
			file_list.append(x)
		elif x.is_dir():
			file_list.extend(searching_all_files(x))
	return file_list

def write_report(inverted_index):
	file = open('inverted_index.txt', 'w')
	max_id = 0
	for key, value in inverted_index.items():
		postings = key
		file.write(key + "\n")
		for posting in value:
			if posting.get_id() > max_id:
				max_id = posting.get_id()
			file.write(str(posting) + "\n")
		file.write("$\n")

	print("Number of Index Documents: ", max_id)
	print("Total Number of Unique Words: ", len(inverted_index))
	p_file = Path('inverted_index.txt') # or Path('./doc.txt')
	size = p_file.stat().st_size
	print("Total Index Size: ", size)
	file.close()


# Stop words: do not use stopping while indexing, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming, but it is up to you to choose.
# Important text: text in bold (b, strong), in headings (h1, h2, h3), and in titles should be treated as more important than the in other places.
# Verify which are the relevant HTML tags to select the important words

if __name__ == '__main__':
	inverted_index = dict()
	start(inverted_index)
	# print(searching_all_files('/home/farbod/Documents/m1_proj/searchEngine/source/sherlock_ics_uci_edu'))
