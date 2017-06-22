"""Write a new json file to update video information.

The new json file will add youtube tariler url based on
original video infomation from IMDB.
"""
from apiclient.discovery import build
from apiclient.errors import HttpError
from os.path import abspath
import argparse
import os
import json
import copy

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyC1VgRvdiTMFRXcQMRATSdlM4-w2KZr8Ss"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Reference:
# https://github.com/youtube/api-samples/blob/master/python/search.py
def youtube_search(options):
    """Return a collection of search results that match the query parameters.

    Args:
        options: arguments for searching video trailer.

    Returns:
        A collection of search results that match the query parameters.

    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results
    ).execute()

    results = search_response.get("items", [])

    return results


def get_youtube_url(video, args):
    """Get youtube url according to video id.

    First, get first video id found in search results that match
    the query parameters.

    Then, get youtube url based on video id.

    Finally, add the youtube url to video dict which already contains relevant
    video infomation from IMDB.

    Args:
        video: a dict contains relevant video infomation from IMDB.
        args: arguments for searching video trailer.

    Returns:
        The video dict that add youtube tariler url based on other relevant
        video infomation from IMDB.

    """
    try:
        search_result = youtube_search(args)

        # There are there kinds of results: channel, playlist and video.
        # A trailer can only belong to video kind.
        # Return the first video id found in search results.
        i = 0
        while i < len(results):
            if search_result[i]["id"]["kind"] == "youtube#video":
                video_id = search_result[i]["id"]["videoId"]
                break
            else:
                i += 1

        print('Get videoId:' + video_id)
        video['trailer'] = 'https://www.youtube.com/watch?v=' + video_id
        return video

    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" %
              (e.resp.status, e.content))


def get_youtube_video(type):
    """Write a new json file to update video information.

    At first, use the information in original json file
    to get youtube trailer url.

    Then write the new json file to add youtube tariler url based on
    original video infomation from IMDB.

    Args:
        type: the video type.
    """
    videos = []
    with open(abspath(os.path.join('data', type + 's_imdb.json'))) as v:
        videos_raw = json.load(v)
        for video in videos_raw:
            # video info provided to youtube_search
            argparser = argparse.ArgumentParser()
            argparser.add_argument("--q", help="Search term", default="Google")
            argparser.add_argument("--max-results",
                                   help="Max results", default=25)
            if type == 'movie':
                args = argparser.parse_args(
                    ["--q", video['title'] + ' trailer'])
                video = get_youtube_url(video, args)
                videos.append(video)
            else:
                for i in range(int(video['season'])):
                    new_video = copy.deepcopy(video)
                    new_title = video['title'] + ' season ' + str(i + 1)
                    new_video['title'] = new_title
                    args = argparser.parse_args(
                        ["--q", new_title + ' trailer'])
                    new_video = get_youtube_url(new_video, args)
                    videos.append(new_video)

        # write to the new json file
        with open(abspath(os.path.join('data',
                                       type + 's_youtube.json')), 'w') as f:
            f.write(json.dumps(videos))


if __name__ == '__main__':
    get_youtube_video('movie')
    get_youtube_video('tv_show')
