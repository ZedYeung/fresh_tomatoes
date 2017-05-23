#! python3
# generate the final fresh_tomatoes html
import json
import os
import re
import webbrowser
import item_class
import fresh_tomatoes

movies = []
tv_shows = []
mv = []

def gen_video_class(type):
    with open(type + 's_youtube.json') as vj:
        videos_raw = json.load(vj)
        for video in videos_raw:
            title = video['title'].replace(' ', '_')
            if type == 'movie':
                locals()[title] = item_class.Movie(*video.values())
                movies.append(locals()[title])
            else:
                locals()[title] = item_class.Tv(*video.values())
                tv_shows.append(locals()[title])

# Problem: can't play mv from VEVO
# This video contains content from VEVO.
# It is restricted from playback on certain sites or applications.
for mv_json in os.listdir('mv'):
    with open(os.path.abspath('.') + '/mv/' + mv_json) as mj:
        mv_raw = json.load(mj)
        # cleaning
        title = mv_raw['title']
        title = re.sub(r'\(.*\)', '', title)
        title = re.sub(r'\[.*\]', '', title)
        title = re.sub(r'(ft\.|feat\.| ft ).*', '', title)
        title = title.replace('|', '-').replace(':', '-')

        # generate object
        summary = title.replace(' ', '_')
        singer, title = title.split('-')
        locals()[summary] = item_class.Mv(title, mv_raw['upload_date'][:4],
                            mv_raw['thumbnail'], mv_raw['webpage_url'],
                            summary, singer)
        mv.append(locals()[summary])

gen_video_class('movie')
gen_video_class('tv_show')

fresh_tomatoes.open_page([movies, tv_shows, mv])
