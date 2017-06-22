#! python3
"""Define classes which objects will be used to fill the fresh_tomatoes html.

There are four kinds of items -- movie, tv show, music video and book will be
displayed on fresh_tomatoes html. Accordingly, there are four kinds of class
that represent these items.
"""
import webbrowser


class Item():
    """Base class."""

    def __init__(self, title, year, poster, url, summary):
        """Constructor.

        Args:
            title: title.
            year: publish year.
            poster: for movie, tv show, music video -- poster.
                    for book -- cover.
            url: for movie, tv show -- youtube trailer url.
                 for music video -- youtube mv url.
                 for book -- local book pdf file path.
            summary: summary, description, storyline.
        """
        self.title = title
        self.year = year
        self.poster = poster
        self.url = url
        self.summary = summary

    def show(self):
        """Show the item in browser."""
        webbrowser.open(self.url)


class Mv(Item):
    """Represent music video."""

    def __init__(self, title, year, poster, url, summary, singer):
        """Constructor.

        Args:
            title: title.
            year: publish year.
            poster: poster.
            url: youtube url.
            summary: description.
            singer: singer, artist, group or band.
        """
        self.singer = singer
        super(Mv, self).__init__(title, year, poster, url, summary)


class Book(Item):
    """Represent book."""

    def __init__(self, title, year, poster, url, summary, author, publisher,
                 page):
        """Constructor.

        Args:
            title: title.
            year: publish year.
            poster: book cover.
            url: local book pdf file path.
            summary: summary, description.
            author: author.
            publisher: publisher.
            page: number of pages.
        """
        self.author = author
        self.publisher = publisher
        self.page = page
        super(Book, self).__init__(title, year, poster, url, summary)


class Video(Item):
    """Represent video.

    Have two subclass that represent movie and tv show respectively.
    """

    def __init__(self, title, year, duration, poster, url, summary, stars):
        """Constructor.

        Args:
            title: title.
            year: publish year.
            duration: duration of feature film -- full-length film.
            poster: poster.
            url: youtube trailer url.
            summary: storyline.
            stars: stars, leading actor/actress.
        """
        self.duration = duration
        self.stars = stars
        super(Video, self).__init__(title, year, poster, url, summary)


class Movie(Video):
    """Represent movie."""

    def __init__(self, title, year, duration, poster, url, summary, director,
                 stars):
        """Constructor.

        Args:
            title: title.
            year: publish year.
            duration: duration of feature film -- full-length film.
            poster: poster.
            url: youtube trailer url.
            summary: storyline.
            director: director.
            stars: stars, leading actor/actress.
        """
        self.director = director
        super(Movie, self).__init__(title, year,
                                    duration, poster, url, summary, stars)


class Tv(Video):
    """Represent tv show."""

    def __init__(self, title, year, duration, poster, url, summary, creator,
                 stars, season, episodes):
        """Constructor.

        Args:
            title: title.
            year: publish year.
            duration: duration of feature film -- full-length film.
            poster: poster.
            url: youtube trailer url.
            summary: storyline.
            creator: a television program creator is typically the person who
                pitches a new TV show idea and sees it through.
            stars: stars, leading actor/actress.
            season: season.
            episodes: number of episodes.
        """
        self.creator = creator
        self.season = season
        self.episodes = episodes
        super(Tv, self).__init__(title, year,
                                 duration, poster, url, summary, stars)
