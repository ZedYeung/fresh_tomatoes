import webbrowser

class Item():
    def __init__(self, title, year, image, url, description):
        self.title = title
        self.year = year
        self.img = image
        self.url = url
        self.desc = description

    def show(self):
        webbrowser.open(self.url)

class Mv(Item):
    def __init__(self, singer):
        self.singer = singer

class Book(Item):
    def __init__(self, author, publisher, page):
        self.author = author
        self.publisher = publisher
        self.page = page

class Video(Item):
    def __init__(self, duration, star):
        self.duration = duration
        self.star = star

class Movie(Video):
    def __init__(self, director):
        self.director = director

class Tv(Video):
    def __init__(self, creator, season, episode):
        self.creator = creator
        self.season = season
        self.episode = episode
