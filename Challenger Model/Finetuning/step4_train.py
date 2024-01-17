"""
Fine-tuning step 4: initiate a fine-tuning job on OpenAI's GPT-3.5 Turbo model using our training file
"""
import openai
import sys

def train(my_api_key, file_id):
    openai.api_key = my_api_key
    response = openai.FineTuningJob.create(training_file = file_id, model = "gpt-3.5-turbo-1106")
    print(response)
    # when the model finished training, an email will be sent to you with the model's id.

if __name__ == "__main__":
    local = False
    if local:
        my_api_key = "YOUR_SECRET_KEY"
    else:
        my_api_key = sys.argv[1]
        file_id = sys.argv[2]
    
    train(my_api_key, file_id)
