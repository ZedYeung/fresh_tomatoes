#! python3

class Item():
    def __init__(self, title, year, poster, url, summary):
        self.title = title
        self.year = year
        self.poster = poster
        self.url = url
        self.summary = summary

    def show(self):
        webbrowser.open(self.url)

class Mv(Item):
    def __init__(self, title, year, poster, url, summary, singer):
        self.singer = singer
        super(Mv, self).__init__(title, year, poster, url, summary)

class Book(Item):
    def __init__(self, author, publisher, page):
        super(Book, self).__init__()
        self.author = author
        self.publisher = publisher
        self.page = page

class Video(Item):
    def __init__(self, title, year, duration, poster, url, summary, stars):
        self.duration = duration
        self.stars = stars
        super(Video, self).__init__(title, year, poster, url, summary)


class Movie(Video):
    def __init__(self, title, year, duration, poster, url, summary, director, stars):
        self.director = director
        super(Movie, self).__init__(title, year, duration, poster, url, summary, stars)


class Tv(Video):
    def __init__(self, title, year, duration, poster, url, summary, creator, stars, season, episodes):
        self.creator = creator
        self.season = season
        self.episodes = episodes
        super(Tv, self).__init__(title, year, duration, poster, url, summary, stars)
