# 121-squad
# Michael Luu, Noah Driker, Farbod Ghiasi, Michael Lofton

import search_engine
import index_builder

def start(inverted_index):
    # inverted_index = build_index(inverted_index)
    # io_manager = search_engine.init()
    # search_engine.get_query_input(io_manager)

    partial_file_names = ["index_A.txt", "index_B.txt", "index_C.txt"]
    index_builder.merge_indices(partial_file_names)
    print("DONE")

def build_index(inverted_index):
    inverted_index = index_builder.indexer(inverted_index)
    index_builder.create_index_squared("inverted_index.txt")
    pass

# Stop words: do not use stopping while indexing, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming, but it is up to you to choose.
# Important text: text in bold (b, strong), in headings (h1, h2, h3), and in titles should be treated as more important than the in other places.
# Verify which are the relevant HTML tags to select the important words

if __name__ == '__main__':
    inverted_index = dict()
    start(inverted_index)
    # print(searching_all_files('/home/farbod/Documents/m1_proj/searchEngine/source/sherlock_ics_uci_edu'))
