# YouTube Sentiment Analyzer

This project outputs data relating to the sentiment of the comments of a YouTube video.

There are 3 files used to achieve this currently:

- download_comments.py : used to download the comments (threads and individual replies) on a YouTube video
- analyze_comments.py : analyzes the resultant data

So far, this script can download the comments of a YouTube video and generate an average of the sentiments of all the comments. This gives us an overall view of how positive/neutral/negative the comments are, which (usually) provides a more accurate metric of the reception of an individual video outside of just likes/dislikes/views.

## APIs/Dependencies Used:

- sklearn
- nltk
- pandas
- YouTube API
