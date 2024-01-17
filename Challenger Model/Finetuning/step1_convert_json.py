"""
Fine-tuning step1: pre-processing training file into json format
"""
import pandas as pd
import json
import sys
from datetime import datetime

def convert_to_json(file_path):
    # target json file path
    today = datetime.today().strftime('%Y%m%d')
    result_path = f'training_data_{today}.json'

    # convert original score to json file for fine-tuning
    data = pd.read_excel(file_path)
    with open(result_path, 'w') as json_file:
        for _, row in data.iterrows():
            article = row['corpora']
            score = row['Scoring']
            cur_data = {"messages": [{"role": "system", "content": "Pretend you are a news analyst."}, 
                    {"role": "user", "content": f"You will rate a news article's sentiment towards Bank of America, or any of its subsidiaries like Merrill Lynch and BofA securities, on a scale from 1-3. 1 = negative, 2 = neutral, 3 = positive. Again, rate sentiment towards BofA in the context of the article and remember only 3 rating choices are allowed (1-3). And give me only the rating number with no additional comments. What would you score for the article below: {article}"}, 
                    {"role": "assistant", "content": f"{score}"}]}
            json.dump(cur_data, json_file)
            json_file.write('\n')
    print(f"convert to json file finished, file saved as {result_path}")

if __name__ == "__main__":
    local = False
    if local:
        # path to the raw training data with Scoring column
        file_path = './2023-12-20_training_set.xlsx'
    else:
        file_path = sys.argv[1]
        
    convert_to_json(file_path)

    