import praw
import pandas as pd
from code import handlers

# REDDIT_CLIENT_ID="FRFFTuIiIcF_yr7FP6iyRg"  # your client id
# REDDIT_CLIENT_SECRET="lshQT_qCF7UOi6MMddnt6jyR-QnC3Q"  # your client secret
# REDDIT_USER_AGENT="Script App"



reddit_read_only = praw.Reddit(client_id="FRFFTuIiIcF_yr7FP6iyRg",  # your client id
                               client_secret="lshQT_qCF7UOi6MMddnt6jyR-QnC3Q",  # your client secret
                               user_agent="Script App")  # your user agent

subreddit = reddit_read_only.subreddit("bitcoin")
#
# # Display the name of the Subreddit
# print("Display Name:", subreddit.display_name)
#
# # Display the title of the Subreddit
# print("Title:", subreddit.title)
#
# # Display the description of the Subreddit
# print("Description:", subreddit.description)

posts = subreddit.top("month")
# Scraping the top posts of the current month

posts_dict = {"Title": [], "Post Text": [],
              "ID": [], "Score": [],
              "Total Comments": [], "Post URL": []
              }

for post in posts:
    # Title of each post
    posts_dict["Title"].append(post.title)

    # Text inside a post
    posts_dict["Post Text"].append(post.selftext)

    # Unique ID of each post
    posts_dict["ID"].append(post.id)

    # The score of a post
    posts_dict["Score"].append(post.score)

    # Total number of comments inside the post
    posts_dict["Total Comments"].append(post.num_comments)

    # URL of each post
    posts_dict["Post URL"].append(post.url)

# Saving the data in a pandas dataframe
top_posts = pd.DataFrame(posts_dict)
print(top_posts)


handlers.write_to_csv(top_posts)


#
# reddit_read_only = praw.Reddit(client_id=credentials.REDDIT_CLIENT_ID,  # your client id
#                                client_secret=credentials.REDDIT_CLIENT_SECRET,  # your client secret
#                                user_agent=credentials.REDDIT_USER_AGENT)	 # your user agent
#
# # URL of the post
# # url = "https://www.reddit.com/r/IAmA/comments/m8n4vt/\
# # im_bill_gates_cochair_of_the_bill_and_melinda/"
#
# url = "https://www.reddit.com/r/datasets/comments/92tlrt/imdb_movies_reviews_dataset_on_kaggle/"
#
# # Creating a submission object
# submission = reddit_read_only.submission(url=url)
#
#
#
# from praw.models import MoreComments
#
# post_comments = []
#
# for comment in submission.comments:
#     if type(comment) == MoreComments:
#         continue
#
#     post_comments.append(comment.body)
#
# # creating a dataframe
# comments_df = pd.DataFrame(post_comments, columns=['comment'])
# print(comments_df)
#
# subreddit = reddit_read_only.subreddit("Python")
#
# posts = subreddit.top("month")
# # Scraping the top posts of the current month
#
# posts_dict = {"Title": [], "Post Text": [],
#               "ID": [], "Score": [],
#               "Total Comments": [], "Post URL": []
#               }
#
# for post in posts:
#     # Title of each post
#     posts_dict["Title"].append(post.title)
#
#     # Text inside a post
#     posts_dict["Post Text"].append(post.selftext)
#
#     # Unique ID of each post
#     posts_dict["ID"].append(post.id)
#
#     # The score of a post
#     posts_dict["Score"].append(post.score)
#
#     # Total number of comments inside the post
#     posts_dict["Total Comments"].append(post.num_comments)
#
#     # URL of each post
#     posts_dict["Post URL"].append(post.url)
#
# # Saving the data in a pandas dataframe
# top_posts = pd.DataFrame(posts_dict)
# top_posts
