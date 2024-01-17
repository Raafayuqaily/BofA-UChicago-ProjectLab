"""
Fine-tuning step 3: Uploading a training file to the OpenAI platform for fine-tuning
"""
import openai
import sys

def upload_training_file(my_api_key, training_json_file):
    openai.api_key = my_api_key
    response = openai.File.create(
        file=open(training_json_file, "rb"),
        purpose="fine-tune"
        )
    print(response)
    # copy the response id into step4_train as our file_id

if __name__ == "__main__":
    local = False
    if local:
        my_api_key = "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"
        # path to the JSON file you want to upload for fine-tuning
        training_json_file = 'training_data_20231222.json'
    else:
        my_api_key = sys.argv[1]
        training_json_file = sys.argv[2]

    upload_training_file(my_api_key, training_json_file)

