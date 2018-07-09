# coding: utf-8
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pickle
from sklearn.externals import joblib
import config

DEVELOPER_KEY = config.api_key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# heavy inspiration from : https://stackoverflow.com/questions/34606055/how-to-get-comments-from-videos-using-youtube-api-v3-and-python

# nltk.download('vader_lexicon')
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def get_video_comments(video_id): # returns a list of comments given a video id
    threads = []
    comments = []
    comment_results = youtube.commentThreads().list( # gets intial batch of comments
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100,
    ).execute()

    for thread in comment_results['items']: # adds to threads and comments
        threads.append(thread)
        comments.append(thread['snippet']['topLevelComment']['snippet']['textDisplay'])

    while 'nextPageToken' in comment_results: # as long as another page is accessible, keep adding to threads and comments
        comment_results = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100,
            pageToken=comment_results['nextPageToken']
        ).execute()
        for thread in comment_results['items']:
            threads.append(thread)
            comments.append(thread['snippet']['topLevelComment']['snippet']['textDisplay'])

    for thread in threads: # get comments out of top level comment threads (replies)
        if(thread['snippet']['totalReplyCount'] > 0):
            replies = youtube.comments().list(
                part='snippet',
                parentId = thread['id']
            ).execute()
            for reply in replies['items']:
                # print(reply)
                comments.append(reply['snippet']['textDisplay'])
    print('Found {} threads with a total of {} comments'.format(len(threads), len(comments)))
    return comments, threads

video_comments, video_threads = get_video_comments('fJP1duVKn7Q')

joblib.dump(video_comments, 'video_comments.pkl') # pickle the comments
joblib.dump(video_threads, 'video_threads.pkl') # pickle the threads

print('PICKLING IS COMPLETE')
