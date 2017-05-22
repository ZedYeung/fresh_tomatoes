import upload_video
import requests
import argparse
import json
import os


def get_html(url):
    html = requests.get(url)
    try:
        html.raise_for_status()
    except Exception as e:
        print('There was a problem: %s' % e)
    return html


def get_youtube_id(type):
    videos = []
    with open(type + 's_imdb.json') as vj:
        videos_raw = json.load(vj)
        for video in videos_raw:
            # download trailer from imdb
            trailer_html = get_html(video['trailer'])
            trailer = os.path.abspath(os.path.join('trailer',
                                    video['title'].replace(' ', '_') + '.mp4'))
            print('Downloading ' + video['title'])
            with open(trailer, 'wb') as t:
                for chunk in trailer_html.iter_content(100000):
                    t.write(chunk)

            # video info provided to youtube
            parser = argparse.ArgumentParser()
            args = parser.parse_args(['--file', trailer])
            args.title = video['title']
            args.description = video['storyline']
            args.category = '44'
            args.keywords = ','.join(video['stars'].extend(
                [video['title'], video['director']]))

            # upload video to get youtube id
            youtube = get_authenticated_service(args)
            try:
                video_id = initialize_upload(youtube, args)
                video['id'] = video_id
                videos.append(video)

                # add video to playlist
                print("adding to playlist...")
                youtube.playlistItems().insert(
                    part='snippet',
                    body=dict(
                        snippet=dict(
                            playlistId='PLAxssHSyCWgJVYOf9OWIzNCfcSYkELvLY' \
                                if type == 'tv_show' else 'PLAxssHSyCWgKtRRt0wZT_oI5WbvOF695Y',
                            resourceId=video_id
                        )
                    )
                )

            except HttpError as e:
                print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

        with open(type + 's_youtube.json', 'w') as f:
            f.write(json.dumps(videos))


if __name__ == '__main__':
    get_youtube_id('movie')
    get_youtube_id('tv_show')
