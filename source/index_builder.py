from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer
from posting import Posting
import json
import re
from pathlib import Path
from string import punctuation
from urllib.parse import urldefrag
import numpy as np


############### MILESTONE 1 #####################
# https://stackoverflow.com/questions/39909655/listing-of-all-files-in-directory
def indexer(inverted_index):
    num_docs_file = open("num_docs.txt", 'w')
    partial_file_names = ["index_A.txt", "index_B.txt", "index_C.txt"]
    doc_id_file = open("doc_ids_urls.txt", "w")
    n = 0

    #/home/fghiasi/M1_project/searchEngine/examples/aiclub_ics_uci_edu
    #/home/fghiasi/inf141Proj2_last_update/inf141Proj2/Assignment3/DEV
    documents = searching_all_files('/home/fghiasi/inf141Proj2_last_update/inf141Proj2/Assignment3/DEV')
    # documents = searching_all_files('/home/fghiasi/testing_M3/searchEngine/examples')
    # documents = ['/home/fghiasi/M1_project/searchEngine/examples/aiclub_ics_uci_edu']

    documents = np.array_split(documents, 3)
    for i, batch in enumerate(documents):
        for document in batch:
            print(document)
            n += 1
            content = extract_json_content(document, 'content')
            url = extract_json_content(document, 'url')

            doc_id_url_str = "{} {}\n".format(n, url)
            doc_id_file.write(doc_id_url_str)

            text, important_dict = tokenize(content)
            word_freq = computeWordFrequencies(text)

            for token in set(text):
                if token not in inverted_index:
                    inverted_index[token] = []
                if token in important_dict:
                    inverted_index[token].append(Posting(n, word_freq[token], important_dict[token]))
                else:
                    inverted_index[token].append(Posting(n, word_freq[token], 0))
        write_partial_index(inverted_index, partial_file_names[i])
        inverted_index = {}
        # inverted_index.clear()
    num_docs_file.write(str(n))
    doc_id_file.close()
    return inverted_index

# def xd():
#     num_docs_file = open("num_docs.txt", 'w')
#     documents = searching_all_files('/home/fghiasi/inf141Proj2_last_update/inf141Proj2/Assignment3/DEV')
#     n = str(len(documents))
#     num_docs_file.write(n)
#     num_docs_file.close()
#
#     partial_file_names = ["index_A.txt", "index_B.txt", "index_C.txt"]
#     merge_indices(partial_file_names)


def merge_indices(partial_file_names):
    file_A = open(partial_file_names[0], 'r')
    file_B = open(partial_file_names[1], 'r')
    file_C = open(partial_file_names[2], 'r')
    inverted_index = open("inverted_index.txt", 'w')

    files = [file_A, file_B, file_C]
    file_lines = [file_A.readline().strip("\n"), file_B.readline().strip("\n"), file_C.readline().strip("\n")]
    # Reset file cursor back to starting position
    for file in files:
        file.seek(0)

    # while file_A_line != '' or file_B_line != '' or file_C_line != '':
    while file_lines[0] != '' or file_lines[1] != '' or file_lines[2] != '':

        file_positions = [ file_A.tell(), file_B.tell(), file_C.tell() ]
        file_lines = [ file_A.readline().strip("\n"), file_B.readline().strip("\n"), file_C.readline().strip("\n") ]

        # Determine and write token
        try:
            earliest_token = min([line for line in file_lines if line != ""]) #min(file_lines) #[file_A_line, file_B_line, file_C_line])
            inverted_index.write(earliest_token + "\n")
        except ValueError:
            return

        postings = []
        for i in range(len(file_lines)):
            if file_lines[i] == earliest_token:
                # Move pointer forward
                # assuming we don't need to preserve doc id order
                # ad-hoc-ly grab the postings and write to inverted_index

                line = file_lines[i] # should be earliest_token
                #line = files[i].readline().strip("\n")
                while line != '$':
                    line = files[i].readline().strip() # read first posting
                    if line != '$':
                        postings.append(line)
            else:
                # reset pointer back
                files[i].seek(file_positions[i]) # EX: file_a.seek(file_a_position)

        for posting in postings:
            inverted_index.write(posting + "\n")

        # write the $ separator
        inverted_index.write("$\n")



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
    # text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
    # text_divs = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))
    text = soup.get_text()

    important_text = (''.join(s.findAll(text=True)) for s in soup.findAll(['strong', "h1", "h2", "h3", "title", "b"]))
    important_dict = dict()

    pattern = "[\s.,!?:;'\"-#$%&<=>@[\\]^_`{|}~]+"
    tokens = list()

    for raw_word in re.split(pattern, text):
        token = raw_word.strip(punctuation).lower()
        if token.isalnum() and re.match("^[a-zA-Z0-9]*$", token) and token != '' and token != '\n':
            word = stemmer.stem(token)
            tokens.append(word)

    # for paragraph in text_p:
    #     for raw_word in re.split(pattern, paragraph):
    #         token = raw_word.strip(punctuation).lower()
    #         if token.isalnum() and re.match("^[a-zA-Z0-9]*$", token) and token != '':
    #             word = stemmer.stem(token)
    #             tokens.append(word)
    #
    # for paragraph in text_divs:
    #     for raw_word in re.split(pattern, paragraph):
    #         token = raw_word.strip(punctuation).lower()
    #         if token.isalnum() and re.match("^[a-zA-Z0-9]*$", token) and token != '':
    #             word = stemmer.stem(token)
    #             tokens.append(word)

    for paragraph in important_text:
        for raw_word in re.split(pattern, paragraph):
            token = raw_word.strip(punctuation).lower()
            if token.isalnum() and re.match("^[a-zA-Z0-9]*$", token) and token != '':
                word = stemmer.stem(token)
                if word in important_dict:
                    important_dict[word] += 1
                else:
                    important_dict[word] = 1

    return tokens, important_dict


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


def write_partial_index(inverted_index, file_name):
    file = open(file_name, 'w')
    for key, value in sorted(inverted_index.items()):
        file.write(key + "\n")
        for posting in value:
            file.write(str(posting) + "\n")
        file.write("$\n")
    file.close()
