# 121-squad
# Michael Luu, Noah Driker, Farbod Ghiasi, Michael Lofton

import search_engine
import index_builder


from app import *
from db_setup import init_db
from forms import MusicSearchForm
from flask import flash, render_template, request, redirect


io_manager = None
init_db()

def start():
    # inverted_index = dict()
    # index_builder.xd()
    # inverted_index = build_index(inverted_index)

    io_manager = search_engine.init()
    search_engine.get_query_input(io_manager)


def build_index(inverted_index):
    inverted_index = index_builder.indexer(inverted_index)
    partial_file_names = ["index_A.txt", "index_B.txt", "index_C.txt"]
    index_builder.merge_indices(partial_file_names)
    index_builder.create_index_squared("inverted_index.txt")
    pass

# Stop words: do not use stopping while indexing, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming, but it is up to you to choose.
# Important text: text in bold (b, strong), in headings (h1, h2, h3), and in titles should be treated as more important than the in other places.
# Verify which are the relevant HTML tags to select the important words




@app.route('/', methods=['GET', 'POST'])
def index():
    print(io_manager == None)
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    query = search.data['search'].strip()
    print("query is: ", search.data['search'])

    results = []


    if query == '':
        # flash('Please Enter your search query.')
        pass
    else:
        search_engine.handle_input(query, io_manager)
        pass

    if not results:
        flash('Search resault 1')
        flash('Search resault 2')
        flash('Search resault 3')
        flash('Search resault 4')
        flash('Search resault 5')
        flash('Search resault 6')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', table=table)


if __name__ == '__main__':
    # inverted_index = dict()
    # start(inverted_index)
    # print(searching_all_files('/home/farbod/Documents/m1_proj/searchEngine/source/sherlock_ics_uci_edu'))
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False

    io_manager = search_engine.init()
    app.run(port=5002)