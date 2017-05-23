#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
import argparse
import json
import copy

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyC1VgRvdiTMFRXcQMRATSdlM4-w2KZr8Ss"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This function partially come from https://github.com/youtube/api-samples/blob/master/python/search.py
# Returns a collection of youtube search results that match the query parameters
def youtube_search(options):
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

    # only the video is possible a trailer
    i = 0
    while i < len(results):
        if results[i]["id"]["kind"] == "youtube#video":
            return results[i]["id"]["videoId"]
        else:
            i += 1


# search to get youtube url according to id
def get_youtube_url(video, args):
    try:
        video_id = youtube_search(args)
        print('Get videoId:' + video_id)
        video['trailer'] = 'https://www.youtube.com/watch?v=' + video_id
        return video

    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" %
              (e.resp.status, e.content))


def get_youtube_video(type):
    videos = []
    with open(type + 's_imdb.json') as vj:
        videos_raw = json.load(vj)
        for video in videos_raw:
            # video info provided to youtube_search
            argparser = argparse.ArgumentParser()
            argparser.add_argument("--q", help="Search term", default="Google")
            argparser.add_argument("--max-results", help="Max results", default=25)
            if type == 'movie':
                args = argparser.parse_args(["--q", video['title'] + ' trailer'])
                video = get_youtube_url(video, args)
                videos.append(video)
            else:
                for i in range(int(video['season'])):
                    new_video = copy.deepcopy(video)
                    new_title = video['title'] + ' season ' + str(i + 1)
                    new_video['title'] = new_title
                    args = argparser.parse_args(["--q", new_title + ' trailer'])
                    new_video = get_youtube_url(new_video, args)
                    videos.append(new_video)

        # write to the new json file
        with open(type + 's_youtube.json', 'w') as f:
            f.write(json.dumps(videos))


if __name__ == '__main__':
    get_youtube_video('movie')
    get_youtube_video('tv_show')
