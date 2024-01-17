import datetime
import sys
import pandas as pd
import requests
import os
import time
import re
from tqdm import tqdm
import datetime

def generate_sentiment_score(new_data):

    url = f'http://localhost:8443/chat'
    size = len(new_data)
    print(f"Received {size} data")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
    result_path_path = f"temp_scores/scores_{timestamp}.txt"
    with open(result_path_path, 'w') as file:
            
        print("----------- Request Sentiment Score from ChatGPT Starts -------------")
        
        with tqdm(total=size, desc="Processing") as pbar:
            for article in new_data:
                time.sleep(0.5) # RPM 500
                data = {
                    'message': f"""
                        Pretend you are a news analyst and you want to rate a news article's sentiment towards Bank of America, or any of its subsidiaries like Merrill Lynch and BofA securities, on a scale from 1-3. \
                        1 = negative, 2 = neutral, 3 = positive. \
                        Again, rate sentiment towards BofA in the context of the article and remember only 3 rating choices are allowed (1-3). \
                        And give me only the rating number with no additional comments. \
                        What would you score for the article below: \
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
                    file.write(f"Error")
                    file.write("\n")
                    
                # Update the progress bar
                pbar.update(1)
        print("-------------- Request Sentiment Score from ChatGPT Ends ----------------")

    return result_path_path

def backtest(testing_file_path):
    data = pd.read_excel(testing_file_path)
    contents = list(data['corpora'])
    result_file_path = generate_sentiment_score(contents)
    sentiment_scores = []
    with open(result_file_path) as my_file:
        for line in my_file:
            sentiment_scores.append(line)
    data['Score_by_ChatGPT'] = sentiment_scores
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
    result_file_path = f'chatGPT_model/results/final_scores/sentiment_scores_by_ChatGPT_{timestamp}.xlsx'
    data.to_excel(result_file_path)
    print(f"data successfully written to {result_file_path}")

if __name__ == "__main__":
    local = False
    if local:
        # path to the testing file
        testing_file_path = '2023-12-20_testing_set.xlsx'
    else:
        testing_file_path = sys.argv[1]

    backtest(testing_file_path)
