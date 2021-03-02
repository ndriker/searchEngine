from collections import namedtuple
from nltk.stem.snowball import SnowballStemmer
from posting import Posting

IOManager = namedtuple('IOManager',
                       ['idx_of_idx_map', 'doc_ids_urls_map', 'idx_of_idx_file', 'inverted_file', 'doc_ids_urls_file'])


############### MILESTONE 2 #####################
def init():
    io_manager = IOManager(None, None, None, None, None)

    inverted_idx_file = open("inverted_index.txt", "r")
    index_of_index_file = open("index_of_index.txt", "r", encoding="utf8")
    ids_urls_file = open("doc_ids_urls.txt", "r")

    # maps
    io_manager = io_manager._replace(idx_of_idx_map=load_index_of_index_map(index_of_index_file))
    io_manager = io_manager._replace(doc_ids_urls_map=load_doc_ids_urls_map(ids_urls_file))

    # files
    io_manager = io_manager._replace(idx_of_idx_file=index_of_index_file)
    io_manager = io_manager._replace(inverted_file=inverted_idx_file)
    io_manager = io_manager._replace(doc_ids_urls_file=ids_urls_file)
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
        index_of_index_map[token] = position  # assuming each line has a unique token
    # print("Done loading index.")
    return index_of_index_map


def load_doc_ids_urls_map(doc_ids_urls_file):
    # doc_ids_urls_file is a file pointer
    doc_ids_urls_map = {}
    for line in doc_ids_urls_file:
        content_list = line.split()  # spaces
        doc_id = content_list[0]
        url = content_list[1]
        doc_ids_urls_map[doc_id] = url  # assuming each line has a unique doc id
    return doc_ids_urls_map


def get_query_input(io_manager):
    while True:
        raw_in = input("Enter your query: ")
        handle_input(raw_in.lower().strip(), io_manager)

def handle_input(raw_input_str, io_manager):
    # assuming input is just words with spaces
    tokens_postings_map = {}
    stemmer = SnowballStemmer(language='english')

    words = raw_input_str.split()  # cristina lopes -> ['cristina', 'lopes']
    # print(words)
    # words = ['we', 'hold', 'workshop']
    for word in words:
        # print("Processing ", word)
        # tokenized_word = tokenize(word) #tokenize & stem the word to match our index
        # #'lopes' -> 'lope'
        stemmed_word = stemmer.stem(word)

        ############# MILE STONE 3 ############
        # word_position = io_manager.idx_of_idx_map[tokenized_word] #find the token's position in inverted_index
        # postings = get_postings(word_position, inverted_file_ptr) #correct O(1) search
        ############# MILE STONE 3 ############

        postings = get_postings(stemmed_word,
                                io_manager.inverted_file)  # O(n) linear search until index_of_index is fixed

        if len(postings) > 0:  # if we have any postings
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
    for i in range(min(5, len(urls))):
        print(i + 1, ": ", urls[i])


def get_urls(intersections, io_manager):
    # O(1)
    urls = []
    for doc_id in intersections:
        if doc_id in io_manager.doc_ids_urls_map:
            urls.append(io_manager.doc_ids_urls_map[doc_id])
    return urls

# O(1) method (FAST)
def get_postings(word_position, inverted_file_ptr):
    print("lol implement me")


# O(n) method (SLOW)
def get_postings(tokenized_word, file_ptr):
    # file_ptr should be inverted_index
    postings = []

    for line in file_ptr:  # "workshop\n"
        line_txt = line.strip("\n")  # "workshop"
        if line_txt == tokenized_word:  # we found the token
            while line_txt != '$':
                line_txt = file_ptr.readline().strip("\n")
                if line_txt != "$":
                    p_values = line_txt.strip().split(',')  # 1,22,1035 -> ['1', '22', '1035']
                    assert 3 == len(p_values)
                    postings.append(Posting(p_values[0], p_values[1], p_values[2]))
            file_ptr.seek(0)
            return postings
    file_ptr.seek(0)
    return postings  # []


def find_word_intersection(tokens_postings_map):
    # print("Finding intersections.")
    list_of_sets = []  # [{4,5,6}, {4,5,6,7}, {1,2,3,4,5}]
    sorted_token_map = sorted(tokens_postings_map.items(), key=(lambda t: len(t[1])))
    for token, postings in sorted_token_map:
        # print("postings", tokens_postings_map[token])

        doc_ids_set = set()
        for posting in postings:
            doc_ids_set.add(posting.get_id())

        list_of_sets.append(doc_ids_set)
    # print(list_of_sets)
    # list_of_sets = [] # [{4,5,6}, {4,5,6,7}, {1,2,3,4,5}]

    first_set = list_of_sets.pop(0)
    tokens_intersection = first_set.intersection(*list_of_sets)  # set of intersected doc ids
    # print(tokens_intersection)
    return tokens_intersection