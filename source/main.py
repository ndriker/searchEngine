from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer

# import urllib.request
import json


def start(inverted_index):
	indexer(inverted_index)


def indexer(inverted_index):

	n = 0
	documents = ['/home/fghiasi/M1_project/searchEngine/source/sherlock_ics_uci_edu/0c2b9a574025e46c443fee02f6269df8f573f95784713e1dbd5c2e2cd07fb6ef.json']
	for document in documents:
		n += 1
		content = extract_json_content(document)

		text = tokonize(content)


def extract_json_content(path):

	file = None
	# https://stackoverflow.com/questions/713794/catching-an-exception-while-using-a-python-with-statement
	try:
		with open(path) as f:
			file = json.load(f)
		print(file['encoding'])
	except EnvironmentError as error:
		print(error, " while reading ", path)
	if file:
		return tokonize(file['content'])



# Tokens: all alphanumeric sequences in the dataset.
def tokonize(html_content):
	soup = BeautifulSoup(html_content, features='html.parser')
	stemmer = SnowballStemmer(language='english')

	tokens = list()
	count = 0
	for word in soup.text.split():
		word = stemmer.stem(word.lower())
		tokens.append(word)
	print(tokens)
	print("Testing")

# Stop words: do not use stopping while indexing, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming, but it is up to you to choose.
# Important text: text in bold (b, strong), in headings (h1, h2, h3), and in titles should be treated as more important than the in other places.
# Verify which are the relevant HTML tags to select the important words

if __name__ == '__main__':
	inverted_index = dict()
	start(inverted_index)