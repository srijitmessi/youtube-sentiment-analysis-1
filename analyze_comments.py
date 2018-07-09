import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import pickle
from sklearn.externals import joblib

video_comments = joblib.load('video_comments.pkl') # pickle the comments
video_threads = joblib.load('video_threads.pkl') # pickle the threads

sid = SentimentIntensityAnalyzer()

sentiments = pd.DataFrame(columns=['Comment', 'Compound', 'Positive', 'Neutral', 'Negative'])

overall_comp = 0.0
overall_pos = 0.0
overall_neu = 0.0
overall_neg = 0.0

for comment in video_comments:
    # print(comment)
    scores = sid.polarity_scores(comment)
    overall_comp += scores['compound']
    overall_pos += scores['pos']
    overall_neu += scores['neu']
    overall_neg += scores['neg']
    sentiments = sentiments.append({'Comment': comment, 'Compound': scores['compound'], 'Positive': scores['pos'], 'Neutral': scores['neu'], 'Negative': scores['neg']}, ignore_index=True)
    # for score in sorted(scores):
    #     print '{}: {}, '.format(score, scores[score]),
    # print('\n')
print('comp:{}, pos:{}, neu:{}, neg:{}'.format(overall_comp / len(video_comments), overall_pos / len(video_comments), overall_neu / len(video_comments), overall_neg / len(video_comments)))
# print(sentiments)

for comment in sentiments.sort_values(by=['Negative'], ascending=False)[0:5].itertuples():
    print(u'-> {}'.format(comment[1]))
