#! python3
# scrawl top rated movie, TV shows sorted by number of ratings on imdb
# Very strange！ requests.get() get incomplete content
# e.g http://www.imdb.com/title/tt0137523/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2398042102&pf_rd_r=17R07QHQG2W885ARH63S&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_10
# #title-overview-widget > div.vital > div.slate_wrapper > div.slate > a
# requests.get() lose whole slate content
# the odd pages 1st, 3rd, etc are completed, but the even pages are incompleted
# I still have no idea why
import time
import json
import requests
from bs4 import BeautifulSoup

movies = []
tv_shows = []
domain = 'http://www.imdb.com'
movie_url = 'http://www.imdb.com/chart/top?sort=nv,desc&mode=simple&page=1'
tv_url = 'http://www.imdb.com/chart/toptv/?sort=nv,desc&mode=simple&page=1'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


def get_html(url):
    html = requests.get(url, headers=headers)
    try:
        html.raise_for_status()
    except Exception as e:
        print('There was a problem: %s' % e)
    return html

# alternative:
# def scrawler(url, top, tv=False, movie=False)
def scrawler(url, top, type):
    # Download the top rating movie or tv_show info and save as json.
    print('Downloading...')

    html = get_html(url)
    soup = BeautifulSoup(html.text, 'lxml')

    title_column = soup.select('.titleColumn')

    if title_column == []:
        print('Could not find resource.')
    else:
        for i in range(top):
            url = title_column[i].select('a')[0].get('href')
            html = get_html(domain + url)
            soup = BeautifulSoup(html.text, 'lxml')

            title = title_column[i].select('a')[0].getText()
            print('Downloading ' + title)
            year = title_column[i].select('span.secondaryInfo')[0].getText()[1:5]
            duration = soup.select('div.title_wrapper div.subtext time[itemprop=duration]')[0].getText().strip()
            poster = soup.select('.poster img')[0].get('src')
            slate = soup.select_one('div.slate > a')
            trailer = domain + slate.get('href') if slate else None
            storyline = soup.select('.summary_text')[0].getText().strip()
            actors = soup.select('.credit_summary_item span[itemprop=actors]')
            stars = [i.getText().strip().replace(',', '') for i in actors]

            if type == 'movie':
                director = soup.select('.credit_summary_item span[itemprop=director]')[0].getText().strip()
                movie = dict(
                    title=title,
                    year = year,
                    duration=duration,
                    poster=poster,
                    trailer=trailer,
                    storyline=storyline,
                    director=director,
                    stars=stars
                )
                movies.append(movie)
            elif type == 'tv':
                creator = soup.select('.credit_summary_item span[itemprop=creator]')
                creator = creator[0].getText().strip() if creator else None
                season = soup.select('#title-episode-widget > div.seasons-and-year-nav > div:nth-of-type(3) > a:nth-of-type(1)')[0].getText()
                episodes = soup.select('div.button_panel a.bp_item span.bp_sub_heading')[0].getText()[:2]
                tv_show = dict(
                    title=title,
                    year=year,
                    duration=duration,
                    poster=poster,
                    trailer=trailer,
                    storyline=storyline,
                    creator=creator,
                    stars=stars,
                    season=season,
                    episodes=episodes
                )
                tv_shows.append(tv_show)
            else:
                print('type = tv or movie')

            time.sleep(1)
    print('Done.')


if __name__ == '__main__':
    scrawler(movie_url, 100, 'movie')
    with open('movies_imdb.json', 'w') as m:
        m.write(json.dumps(movies))

    scrawler(tv_url, 50, 'tv')
    with open('tv_shows_imdb.json', 'w') as t:
        t.write(json.dumps(tv_shows))
