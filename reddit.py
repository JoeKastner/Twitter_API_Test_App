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
import json
import datetime

#%%
with open('passwords.json') as f:
  data = json.load(f)

client_id = data['reddit']['client_id']
client_secret = data['reddit']['client_secret']

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='my user agent')

comments = collections.defaultdict(list)
for comment in reddit.subreddit('all').search(query='author:StringCheeseInc', limit=100, time_filter='all', sort='new'):
    comments['subreddit'].append(comment.subreddit.display_name)
    comments['title'].append(comment.title)
    comments['author'].append(comment.author)
    comments['linked_url'].append(comment.url)
    comments['reddit_url'].append('https://www.reddit.com' + comment.permalink)
    comments['upvotes'].append(comment.ups)
    comments['downvotes'].append(comment.downs)
    comments['sumvotes'].append(comment.ups - comment.downs)
    comments['total_awards_received'].append(comment.total_awards_received)
    comments['num_comments'].append(comment.num_comments)
    comments['subreddit_name_prefixed'].append(comment.subreddit_name_prefixed)
    comments['domain'].append(comment.domain)
    comments['subreddit_subscribers'].append(comment.subreddit_subscribers)
    comments['created_utc'].append(datetime.datetime.utcfromtimestamp(comment.created_utc))
                                   
df = pd.DataFrame.from_dict(comments)

import seaborn as sns 
import matplotlib.pyplot as plt
sns.set(style="whitegrid", 
        rc={"lines.linewidth": 4,
            "figure.figsize":(10, 8)})


sns.lineplot(x = df.created_utc, y = df.upvotes, color='#069bd7', alpha=0.75, marker="o", markersize=7)
sns.lineplot(x = df.created_utc, y = df.num_comments, color='orange', alpha=0.75, marker="o", markersize=7)
plt.legend(labels=['Upvotes', '# Comments'])
plt.ylabel("")
plt.xlabel("Post Date")
plt.tick_params(labelsize=12)
plt.title("Upvotes and Comments over time for " + comment.author.name, size=16)


# %%



# sns.scatterplot(x=df.upvotes, y=df.num_comments)

# %%
sns.PairGrid(df)

# %%
