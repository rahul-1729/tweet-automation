from autogen import AssistantAgent, UserProxyAgent,GroupChat, GroupChatManager
from constants import number_of_days, times_per_day
from prompt import BUSSINESS_DESCRIPTION, CRITIC_PROMPT, TAGGER_PROMPT, WRITER_PROMPT, USER_PROXY_PROMPT
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# from configs.gemini_config import OAI_CONFIG_LIST

seed = 44

llm_config_gemini = {
    "config_list" : [
    {
        "model": "gemini-2.0-flash",
        "api_key": GEMINI_API_KEY,
        "api_type": "google"
    }
],
    "seed" : seed
}


 
user_proxy = UserProxyAgent(
    name="UserProxy",
    llm_config=llm_config_gemini,
    human_input_mode="NEVER",
    code_execution_config={"work_dir": ".", "use_docker": False},
    system_message=USER_PROXY_PROMPT
)



content_researcher = AssistantAgent(
    name="ContentResearcher",
    llm_config=llm_config_gemini,
    system_message=BUSSINESS_DESCRIPTION,

)

content_writer = AssistantAgent(
    name="ContentWriter",
    llm_config=llm_config_gemini,
    system_message=WRITER_PROMPT
)

tweet_tagger = AssistantAgent(
    name="TweetTagger",
    llm_config=llm_config_gemini,
    system_message=TAGGER_PROMPT
)

content_critic = AssistantAgent(
    name="ContentCritic",
    llm_config=llm_config_gemini,
    system_message= CRITIC_PROMPT
)

agents = [user_proxy,content_researcher, content_writer,tweet_tagger, content_critic]

chat = GroupChat(
    agents=agents,
    messages=[],
    max_round=5,  # Reduced rounds to avoid empty responses
    speaker_selection_method="round_robin"
)

manager = GroupChatManager(
    groupchat=chat,
    llm_config=llm_config_gemini
)

def extract_final_tweet(chat_result):
    """Extract the final tweet from chat history"""
    chat_history = chat_result.chat_history
    
    # Look for the last message from ContentCritic (final reviewer)
    for message in reversed(chat_history):
        if message.get('name') == 'ContentCritic' and message.get('content'):
            content = message['content'].strip()
            if content and len(content) <= 280:
                return content
    
    # Fallback: Look for the last ContentWriter message
    for message in reversed(chat_history):
        if message.get('name') == 'ContentWriter' and message.get('content'):
            content = message['content'].strip()
            if content and len(content) <= 280:
                return content
    
    # Fallback: Look for any message with reasonable tweet length and hashtags
    for message in reversed(chat_history):
        content = message.get('content', '').strip()
        if content and '#' in content and 50 <= len(content) <= 280:
            return content
    
    # Last resort: Get the summary or first meaningful content
    if hasattr(chat_result, 'summary') and chat_result.summary:
        return chat_result.summary.get('content', 'No tweet generated')
    
    return "No tweet generated"

def generate_tweet():
    """Generate a single tweet"""
    initial_message = BUSSINESS_DESCRIPTION

    # Start the conversation
    chat_result = user_proxy.initiate_chat(
        manager,
        message=initial_message,
        summary_method="reflection_with_llm",
    )
    
    # Extract the final tweet
    final_tweet = extract_final_tweet(chat_result)
    return final_tweet

if __name__ == "__main__":
    # Test the tweet generation
   
    number_of_tweets = number_of_days * times_per_day
    
    for tweet in range(number_of_tweets):
        tweet = generate_tweet()
        print(f"\nFinal Tweet:")
        print(f"'{tweet}'")
   
 