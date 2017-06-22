"""Generate the final fresh_tomatoes html.

Use data in data directory to create according class objects and then
use them to fill the fresh_tomatoes html frame.
"""
import json
import os
import re
import webbrowser
import item_class
import fresh_tomatoes
from os.path import abspath

# list that store objects of specific item class.
movies = []
tv_shows = []
mv = []
books = []


def create_video_obj(subclass):
    """Create objects of certain Video subclass."""
    with open(abspath(os.path.join('data', subclass + 's_youtube.json'))) as v:
        videos_raw = json.load(v)
        for video in videos_raw:
            title = video['title'].replace(' ', '_')
            if subclass == 'movie':
                locals()[title] = item_class.Movie(*video.values())
                movies.append(locals()[title])
            else:
                locals()[title] = item_class.Tv(*video.values())
                tv_shows.append(locals()[title])


# Create objects of Mv class.
# Problem: can't play mv from VEVO.
# This video contains content from VEVO.
# It is restricted from playback on certain sites or applications.
for mv_json in os.listdir('./data/mv'):
    with open(abspath(os.path.join('data', 'mv', mv_json))) as m:
        mv_raw = json.load(m)
        # cleaning
        title = mv_raw['title']
        title = re.sub(r'\(.*\)', '', title)
        title = re.sub(r'\[.*\]', '', title)
        title = re.sub(r'(ft\.|feat\.| ft ).*', '', title)
        title = title.replace('|', '-').replace(':', '-')

        # create object
        summary = title.replace(' ', '_')
        singer, title = title.split('-')
        locals()[summary] = item_class.Mv(title,
                                          mv_raw['upload_date'][:4],
                                          mv_raw['thumbnail'],
                                          mv_raw['webpage_url'],
                                          summary, singer)
        mv.append(locals()[summary])

# Create objects of Book class.
with open(abspath(os.path.join('data', 'origin_book_info.json'))) as b:
    books_info = json.load(b)
    for book_info in books_info:
        title = book_info['title'].replace(' ', '_')
        year = book_info['pubdate'][:4]
        poster = book_info['images']['large']
        url = abspath(os.path.join('data', 'pdf', title + '.pdf'))
        summary = book_info['summary']
        author = book_info['author']
        publisher = book_info['publisher']
        page = book_info['pages']
        locals()[title] = item_class.Book(book_info['title'],
                                          year, poster, url, summary,
                                          author, publisher, page)
        books.append(locals()[title])

create_video_obj('movie')
create_video_obj('tv_show')

# Fill the fresh_tomatoes html frame with item objects.
fresh_tomatoes.open_page([movies, tv_shows, mv, books])
