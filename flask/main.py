# main.py

from app import app
from db_setup import init_db, db_session
from forms import MusicSearchForm
from flask import flash, render_template, request, redirect
from models import Album
from app import io_manager
# from searchEngine.source import search_engine

init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    print(io_manager)
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    print("query is: ", search.data['search'])
    results = []
    search_string = search.data['search']

    if search_string == '':
        # flash('Please Enter your search query.')
        pass
    else:

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
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    app.run(port=5001)