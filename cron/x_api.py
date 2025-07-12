import tweepy
import os
import dotenv

dotenv.load_dotenv()

# Your secrets (keep these safe!)
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
 

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

def post_tweet(content):
    """Post a tweet using the Tweepy client."""
    try:
        response = client.create_tweet(text=content)
        print(f"Tweet posted successfully: {response.data['text']}")
        return True
    except Exception as e:
        print(f"An error occurred while posting the tweet: {e}")
        return False

 