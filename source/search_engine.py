from collections import namedtuple
from nltk.stem.snowball import SnowballStemmer
from posting import Posting
import time
import math
from collections import defaultdict
stop_words = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
              "as", "at", "be", "because", "been",
              "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did",
              "didn't", "do", "does", "doesn't", "doing",
              "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
              "have", "haven't", "having", "he", "he'd", "he'll",
              "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd",
              "i'll", "i'm", "i've", "if", "in", "into", "is",
              "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no",
              "nor", "not", "of", "off", "on", "once", "only",
              "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
              "she'd", "she'll", "she's", "should", "shouldn't",
              "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
              "there", "there's", "these", "they", "they'd",
              "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very",
              "was", "wasn't", "we", "we'd", "we'll", "we're",
              "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while",
              "who", "who's", "whom", "why", "why's", "with",
              "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
              "yourselves"}

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


def get_query_input(io_manager, query):
    # while True:
    #     raw_in = input("Enter your query: ")
    #     handle_input(raw_in.lower().strip(), io_manager)
    pass

def handle_input(raw_input_str, io_manager):
    start_time = time.time()
    # assuming input is just words with spaces
    tokens_postings_map = {}
    stemmer = SnowballStemmer(language='english')
    words = [word for word in raw_input_str.split() if word not in stop_words]
    # words = raw_input_str.split()  # cristina lopes -> ['cristina', 'lopes']
    # print(words)
    # words = ['we', 'hold', 'workshop']
    for word in words:
        # print("Processing ", word)
        # tokenized_word = tokenize(word) #tokenize & stem the word to match our index
        # #'lopes' -> 'lope'
        stemmed_word = stemmer.stem(word)

        ############# MILE STONE 3 ############
        try:
            word_position = int(io_manager.idx_of_idx_map[stemmed_word]) #find the token's position in inverted_index
        except KeyError:
            continue
        postings = get_postings(word_position, io_manager.inverted_file) #correct O(1) search
        ############# MILE STONE 3 ############

        # postings = get_postings(stemmed_word,
        #                         io_manager.inverted_file)  # O(n) linear search until index_of_index is fixed

        if len(postings) > 0:  # if we have any postings
            # Assumes all words are unique
            tokens_postings_map[stemmed_word] = postings
        # print(tokens_postings_map)
    # else, no postings
    # no results

    # find intersection of posting objects, sort postings by word frequency
    intersections = find_word_intersection(tokens_postings_map)

    doc_ids_score_map = calculate_ranking(tokens_postings_map, intersections)
    # print("intersections", intersections)
    urls = get_urls(doc_ids_score_map, io_manager)
    end_time = time.time()
    # print(urls)
    print_urls(urls)
    print("Time: ", end_time - start_time)


def print_urls(urls):
    for i in range(min(5, len(urls))):
        print(i + 1, ": ", urls[i])


def get_urls(doc_ids_score_map, io_manager):
    # O(1)
    urls = []

    for doc_id in sorted(doc_ids_score_map, key=doc_ids_score_map.get, reverse=True):
        if doc_id in io_manager.doc_ids_urls_map:
            urls.append(io_manager.doc_ids_urls_map[doc_id])
    return urls

# O(1) method (FAST)
def get_postings(word_position, inverted_file_ptr):
    postings = []

    inverted_file_ptr.seek(word_position)
    line = inverted_file_ptr.readline().strip()
    while line != '$':
        line = inverted_file_ptr.readline().strip()
        if line != '$':
            p_values = line.strip().split(',')  # 1,22,1035 -> ['1', '22', '1035']
            print(p_values)
            print(word_position)
            assert 3 == len(p_values)
            postings.append(Posting(p_values[0], p_values[1], p_values[2]))
    return postings


# O(n) method (SLOW)
# def get_postings(tokenized_word, file_ptr):
#     # file_ptr should be inverted_index
#     postings = []
#
#     for line in file_ptr:  # "workshop\n"
#         line_txt = line.strip("\n")  # "workshop"
#         if line_txt == tokenized_word:  # we found the token
#             while line_txt != '$':
#                 line_txt = file_ptr.readline().strip("\n")
#                 if line_txt != "$":
#                     p_values = line_txt.strip().split(',')  # 1,22,1035 -> ['1', '22', '1035']
#                     assert 3 == len(p_values)
#                     postings.append(Posting(p_values[0], p_values[1], p_values[2]))
#             file_ptr.seek(0)
#             return postings
#     file_ptr.seek(0)
#     return postings  # []


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

    ###############################################################################
    # machine: 5 times
    # learning: 5 times
    # tf: 10
    # intersection: {4}

    # go through doc ids in intersection
    # find postings (FROM OUR QUERY TERMS) with same doc id
    # accumulate the TF (freq_counts) for that posting for that doc id

    # doc_id_sum = {}
    # for token, postings in tokens_postings_map:
    #     for posting in postings: #no duplicates
    #         if posting.doc_id in intersection: #no summing twice or more
    #             doc_id_sum[posting.doc_id] += posting.freq_counts

    # Ranking function from Lec 20:
    # wt,d = (1+log(tft,d)) x log(N/dft)
    ###############################################################################
    try:
        first_set = list_of_sets.pop(0)
    except IndexError:
        print("No results found.")
        return set()
    tokens_intersection = first_set.intersection(*list_of_sets)  # set of intersected doc ids
    # print(tokens_intersection)
    return tokens_intersection

def compute_tf_idf_weight_score(term_frq, doc_freq, n):
    return 1 + math.log(int(term_frq), 10) * math.log(int(n) / int(doc_freq), 10)

# Incorporating important words
def compute_important_words(important_counter):
    important_counter = int(important_counter)
    if important_counter != 0:
        return 1 + math.log(important_counter, 10) #if 100, then -> 1 + 2 = 3
    return 0

def calculate_ranking(tokens_posting_maps, intersections):
    doc_id_score_map = defaultdict(int) # default dict of ints
    # Intersections {4,5,6}

    # {4: 5} Master: 5, Software: 5, Engineering: 10
    # {5: 0}
    # {6: 0}

    # Master, software, Engineering
    for tokens,postings in tokens_posting_maps.items():
        for post in postings: # Software's list of postings [1,4,5,6,9] |   #Master [1,2,3,4,5,6,7]
            if post.doc_id in intersections: # O(1)
                tf = post.get_freq()
                df = len(postings)
                doc_id_score_map[post.doc_id] += compute_tf_idf_weight_score(tf, df, 55393)
                doc_id_score_map[post.doc_id] += compute_important_words(post.important_counter)
                # {4: 20 (Master: 5, Software: 5, Engineering: 10)}
    return doc_id_score_map
    # END RESULT:
    # {4: 20}
    # {5: 10}
    # {6: 15}

    # Sorted map:
    # {5: 10}
    # {6: 15}
    # {4: 20}

    # in handle_input"
    # pass map of rankings to get_urls
    # sort map of rankings in get_urls
    # gets urls in order based on the sorting