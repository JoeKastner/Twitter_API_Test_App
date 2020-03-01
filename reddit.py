#%%

'''
Author: Joe Kastner
Date: 2/29/20
Description: Search Reddit via api and praw library for keywords, package results into 
    dataframe and load into database
'''

import praw
import collections
import pandas as pd

#%%

reddit = praw.Reddit(client_id='AD-EHj4oEX4DmQ',
                     client_secret='cKfygcej8h8t7DTFekJ-iQSvurQ',
                     user_agent='my user agent')

# %%
my_keywords = ['test']

for comment in reddit.subreddit('all').stream.comments():
     cbody = comment.body
     if any(keyword in cbody for keyword in my_keywords):
         print(comment)

# %%
comments = collections.defaultdict(list)
for comment in reddit.subreddit('all').search(query='Con Edison'):
    comments['subreddit'].append(comment.subreddit.display_name)
    comments['title'].append(comment.title)
    comments['author'].append(comment.author)
    comments['linked_url'].append(comment.url)
    comments['reddit_url'].append('https://www.reddit.com' + comment.permalink)
    comments['upvotes'].append(comment.ups)
    comments['total_awards_received'].append(comment.total_awards_received)
    comments['num_comments'].append(comment.num_comments)
    comments['subreddit_name_prefixed'].append(comment.subreddit_name_prefixed)
    comments['domain'].append(comment.domain)
    comments['subreddit_subscribers'].append(comment.subreddit_subscribers)
    comments['created_utc'].append(comment.created_utc)


#%%
df = pd.DataFrame.from_dict(comments)





# %%
