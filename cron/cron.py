import sys
import os

from x_api import post_tweet
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import pytz
import requests
from datetime import datetime
from dotenv import load_dotenv

 
load_dotenv()

 
IST = pytz.timezone('Asia/Kolkata')

 
GOOGLE_SHEET_API = os.getenv("GOOGLE_SHEET_LINK")
SCHEDULED_TIME = ['09:00', '11:00', '15:00']

def fetch_pending_tweets():
    """Fetch pending tweets from Google Sheets"""
    try:

        # GET request to fetch pending tweets
        response = requests.get(GOOGLE_SHEET_API)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'success':
                pending_tweets = data.get('data', [])
                print(f"Found {len(pending_tweets)} pending tweets")
                return pending_tweets
            else:
                print(f"Error from API: {data.get('message', 'Unknown error')}")
                return []
        else:
            print(f"Failed to fetch tweets. Status code: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching tweets: {str(e)}")
        return []

def update_tweet_status(tweet_id):
    """Update tweet status to 'done' using PUT request"""
    try:
        print(f"Updating tweet {tweet_id} status to 'done'...")
        
        # Prepare payload for status update
        payload = {
            "tweet_id": tweet_id,
            "status": "done",
            "task": "update_tweet"
        }

        # Make POST request to update status
        response = requests.post(GOOGLE_SHEET_API, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                print(f" Tweet {tweet_id} status updated to done")
                return True
            else:
                print(f" Failed to update: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"Failed to update tweet {tweet_id}. Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f" Error updating tweet status: {str(e)}")
        return False

def process_and_post_tweets():
    """Main function to fetch pending tweets, post them, and update status"""
    current_time = datetime.now(IST).strftime('%d/%m/%Y %H:%M:%S IST')
    print(f"\n Starting tweet processing at {current_time}")
    print("=" * 60)
    
    # Fetch pending tweets from Google Sheets
    pending_tweets = fetch_pending_tweets()
    
    if not pending_tweets:
        print("📭 No pending tweets found")
        return

    tweet_data = pending_tweets[0]

    tweet_id = str(tweet_data.get('tweet_id', ''))
    tweet_content = str(tweet_data.get('tweet', ''))
    
    print(f" Processing Tweet ID: {tweet_id}")
    print(f"Content: {tweet_content}")
    
    # Post tweet to Twitter
    print(f"Posting tweet to Twitter...")
    
    try:
        # Call your Twitter API function
        success = post_tweet(tweet_content)
        print(success)

        if success:
            print(f" Tweet posted successfully!")
       
            
            # Update status to 'done' in Google Sheets
            update_success = update_tweet_status(tweet_id)
            
            
            
        else:
            print(f" Failed to post tweet {tweet_id}")
    
            # Optionally update status to 'failed'
            
            
    except Exception as e:
        print(f" Error posting tweet {tweet_id}: {str(e)}")
  
        
    
    print("-" * 40)
  

 

 

def start_specific_time_cron():
    """Start scheduler that runs at specific times in IST"""
    scheduler = BlockingScheduler()
    
    # Schedule tweets at specific times (modify as needed)
    # Example: Every day at 9:00 AM, 3:09 PM, and 6:00 PM IST
    times_to_run = SCHEDULED_TIME

    for time_str in times_to_run:
        hour, minute = map(int, time_str.split(':'))
        scheduler.add_job(
            func=process_and_post_tweets,
            trigger='cron',
            hour=hour,
            minute=minute,
            timezone=IST,
            id=f'tweet_job_{time_str}',
            name=f'Process tweets at {time_str} IST'
        )
    
    print("🕐 Starting specific time tweet automation...")
    print(f"📅 Will process tweets at: {', '.join(times_to_run)} IST daily")
    print("⏰ Press Ctrl+C to stop")
    print("-" * 60)
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\n🛑 Specific time scheduler stopped by user")
        scheduler.shutdown()

if __name__ == "__main__":
    start_specific_time_cron()