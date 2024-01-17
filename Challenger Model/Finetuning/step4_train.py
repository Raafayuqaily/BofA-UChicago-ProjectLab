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
        my_api_key = "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"
        # file_id = "file-3KSl05aDNHfyLZCvvifizWvG"
        # file_id = "file-jjDF2ZnSi5q90eXuyiWImAdu"
        file_id = "file-ozSBt2Fqp2PNVUegbDTLZom2"

    else:
        my_api_key = sys.argv[1]
        file_id = sys.argv[2]
    
    train(my_api_key, file_id)