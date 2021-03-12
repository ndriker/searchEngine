# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# import source.search_engine
# import searchEngine.source.search_engine

io_manager = None

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mymusic.db'
app.secret_key = "flask rocks!"

db = SQLAlchemy(app)


# io_manager = searchEngine.source.search_engine.init()
