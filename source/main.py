# 121-squad
# Michael Luu, Noah Driker, Farbod Ghiasi, Michael Lofton
from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer
from posting import Posting
import json
from pathlib import Path
import re
from string import punctuation
from urllib.parse import urldefrag
from collections import namedtuple

IOManager = namedtuple('IOManager', ['idx_of_idx_map','doc_ids_urls_map', 'idx_of_idx_file', 'inverted_file', 'doc_ids_urls_file'])

def start(inverted_index):
	#inverted_index = indexer(inverted_index)
	#write_report(inverted_index)
	#create_index_squared("inverted_index.txt")
	# print(indexer(inverted_index))

	#inverted_file = open("inverted_index.txt", "r")
	io_manager = init()
	# print("init done")
	get_query_input(io_manager)

############### MILESTONE 2 #####################
def init():
	io_manager = IOManager(None, None, None, None, None)

	inverted_idx_file = open("inverted_index.txt", "r")
	index_of_index_file = open("index_of_index.txt", "r", encoding="utf8")
	ids_urls_file = open("doc_ids_urls.txt", "r")

	# maps
	io_manager = io_manager._replace(idx_of_idx_map = load_index_of_index_map(index_of_index_file))
	io_manager = io_manager._replace(doc_ids_urls_map = load_doc_ids_urls_map(ids_urls_file))

	# files
	io_manager = io_manager._replace(idx_of_idx_file = index_of_index_file)
	io_manager = io_manager._replace(inverted_file = inverted_idx_file)
	io_manager = io_manager._replace(doc_ids_urls_file = ids_urls_file)
	# print("io manager", io_manager)
	return io_manager

def load_index_of_index_map(index_of_index_file):
	index_of_index_map = {}
	line_counter = 0
	line_num = 0

	path = "index_of_index.txt"
	for line in index_of_index_file:
		line_counter += len(line)
		# print("byte", line_counter, "line #", line_num)

		line_num += 1

		content_list = line.split()  # spaces
		token = content_list[0]
		position = content_list[1]
		index_of_index_map[token] = position # assuming each line has a unique token
	# print("Done loading index.")
	return index_of_index_map

def load_doc_ids_urls_map(doc_ids_urls_file):
	# doc_ids_urls_file is a file pointer
	doc_ids_urls_map = {}
	for line in doc_ids_urls_file:
		content_list = line.split() #spaces
		doc_id = content_list[0]
		url = content_list[1]
		doc_ids_urls_map[doc_id] = url # assuming each line has a unique doc id
	return doc_ids_urls_map

def get_query_input(io_manager):
	while True:
		raw_in = input("Enter your query: ")
		handle_input(raw_in.lower(), io_manager)
		# print("Getting query input for: \n", raw_in)


def handle_input(raw_input_str, io_manager):
	# assuming input is just words with spaces
	tokens_postings_map = {}

	stemmer = SnowballStemmer(language='english')

	words = raw_input_str.split() #cristina lopes -> ['cristina', 'lopes']
	# print(words)
	# words = ['we', 'hold', 'workshop']
	for word in words:
		# print("Processing ", word)
		# tokenized_word = tokenize(word) #tokenize & stem the word to match our index
		# #'lopes' -> 'lope'
		stemmed_word = stemmer.stem(word)

		############# MILE STONE 3 ############
		#word_position = io_manager.idx_of_idx_map[tokenized_word] #find the token's position in inverted_index
		#postings = get_postings(word_position, inverted_file_ptr) #correct O(1) search
		############# MILE STONE 3 ############

		postings = get_postings(stemmed_word, io_manager.inverted_file) #O(n) linear search until index_of_index is fixed
		# print(stemmed_word, postings)

		if len(postings) > 0: #if we have any postings
			# Assumes all words are unique
			tokens_postings_map[stemmed_word] = postings
			# print(tokens_postings_map)
		# else, no postings
		# no results

	# find intersection of posting objects, sort postings by word frequency
	intersections = find_word_intersection(tokens_postings_map)
	# print("intersections", intersections)
	urls = get_urls(intersections, io_manager)
	# print(urls)
	print_urls(urls)

def print_urls(urls):

	for i in range(5):
		print(i + 1 , ": ", urls[i])

def get_urls(intersections, io_manager):
	# O(1)
	urls = []
	for doc_id in intersections:
		if doc_id in io_manager.doc_ids_urls_map:
			urls.append(io_manager.doc_ids_urls_map[doc_id])
	return urls


def get_postings(tokenized_word, file_ptr):
	# file_ptr should be inverted_index
	postings = []

	for line in file_ptr: #"workshop\n"
		line_txt = line.strip("\n") #"workshop"
		if line_txt == tokenized_word: #we found the token
			while line_txt != '$':
				line_txt = file_ptr.readline().strip("\n")
				if line_txt != "$":
					p_values = line_txt.strip().split(',')  # 1,22,1035 -> ['1', '22', '1035']
					assert 3 == len(p_values)
					postings.append(Posting(p_values[0], p_values[1], p_values[2]))
			file_ptr.seek(0)
			return postings
	file_ptr.seek(0)
	return postings # []

def find_word_intersection(tokens_postings_map):
	# print("Finding intersections.")
	list_of_sets = []  # [{4,5,6}, {4,5,6,7}, {1,2,3,4,5}]
	sorted_token_map = sorted(tokens_postings_map.items(), key=(lambda t: len(t[1])))
	for token,postings in sorted_token_map:
		# print("postings", tokens_postings_map[token])

		doc_ids_set = set()
		for posting in postings:
			doc_ids_set.add(posting.get_id())

		list_of_sets.append(doc_ids_set)
	# print(list_of_sets)

	# list_of_sets = [] # [{4,5,6}, {4,5,6,7}, {1,2,3,4,5}]

	first_set = list_of_sets.pop(0)
	tokens_intersection = first_set.intersection(*list_of_sets) #set of intersected doc ids
	# print(tokens_intersection)
	return tokens_intersection

############### MILESTONE 1 #####################
# https://stackoverflow.com/questions/39909655/listing-of-all-files-in-directory
def indexer(inverted_index):
	doc_id_file = open("doc_ids_urls.txt", "w")
	n = 0

	#/home/fghiasi/M1_project/searchEngine/examples/aiclub_ics_uci_edu
	#/home/fghiasi/inf141Proj2_last_update/inf141Proj2/Assignment3/DEV
	#dev_path = "C:\\Users\\NoobMaster69\\Desktop\\School\\CS 121 - Info Retrieval\\Assignments\\3-Search-Engine\\M1\\developer\\DEV"
	dev_path = "doh"
	documents = searching_all_files(dev_path)
	#documents = searching_all_files('/home/fghiasi/inf141Proj2_last_update/inf141Proj2/Assignment3/DEV')
	# documents = ['/home/fghiasi/M1_project/searchEngine/examples/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json']

	for document in documents:
		n += 1
		content = extract_json_content(document, 'content')
		url = extract_json_content(document, 'url')

		doc_id_url_str = "{} {}\n".format(n, url)
		doc_id_file.write(doc_id_url_str)

		text = tokenize(content)
		word_freq = computeWordFrequencies(text)

		for i, token in enumerate(text):
			if token not in inverted_index:
				inverted_index[token] = []
			inverted_index[token].append(Posting(n, word_freq[token], i))
			# print(token, " ", Posting(n, word_freq[token], i))
	doc_id_file.close()
	return inverted_index


def extract_json_content(path, data_type):
	file = None
	# https://stackoverflow.com/questions/713794/catching-an-exception-while-using-a-python-with-statement
	try:
		with open(path) as f:
			file = json.load(f)
	except EnvironmentError as error:
		print(error, " while reading ", path)
	if file:
		if data_type == 'content':
			return file['content']
		elif data_type == 'url':
			try:
				return urldefrag(file['url']).url
			except Exception as ex:
				print(ex)
				return None

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
			# for windows: postingsSize += len(line) + 1
			postingsSize += len(line)
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
def tokenize(html_content):
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
