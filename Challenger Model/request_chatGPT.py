import requests
import os
import time
import re
from tqdm import tqdm
from datetime import datetime

def generate_sentiment_score(new_data):

    # server_ip = os.getenv("MY_SERVER_IP")
    # if server_ip is None:
    #     raise ValueError("Environment variable MY_SERVER_IP is not set.")

    url = f'http://localhost:8443/chat'
    size = len(new_data)
    print(f"Received {size} data")
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    result_path_path = f"temp_scores/scores_{timestamp}.txt"
    with open(result_path_path, 'w') as file:
            
        print("----------- Request Sentiment Score from ChatGPT Starts -------------")
        
        with tqdm(total=size, desc="Processing") as pbar:
            for article in new_data:
                time.sleep(0.12) # RPM 500
                data = {
                    'message': f"""
                        Pretend you are a news analyst and you want to rate a news article's sentiment towards Bank of America, or any of its subsidiaries like Merrill Lynch and BofA securities, on a scale from 1-5. \
                        1 = very negative, 2 = slightly negative/negative, 3 = neutral, 4 = slightly positive/positive, 5 = very positive. \
                        Again, rate sentiment towards BofA in the context of the article and remember only 5 rating choices are allowed (1-5). \
                        And give me only the rating number with no additional comments. \
                        What would you score for the article below: 
                        {article}"""
                }
                response = requests.post(url, json=data)
                
                if response.status_code == 200:
                    print('POST request was successful')
                    feedback =  response.json()['feedback'].lower()
                    print(f"feedback: {feedback}")
                    match = re.search(r'\d', feedback)
                    if match:
                        sentiment_score = match.group()
                        print("Sentiment score found:", sentiment_score)
                        file.write(sentiment_score)
                        file.write("\n")
                    else:
                        print("Sentiment score not found")
                        file.write("Not Found")
                        file.write("\n")
                else:
                    print('POST request failed with status code:', response.status_code)
                    print('Response content:', response.text)
                    file.write(f"Context too long")
                    file.write("\n")
                    
                # Update the progress bar
                pbar.update(1)
        print("-------------- Request Sentiment Score from ChatGPT Ends ----------------")

    return result_path_path