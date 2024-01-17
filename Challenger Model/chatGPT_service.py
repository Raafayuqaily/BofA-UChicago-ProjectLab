import os
from flask import Flask, request, jsonify
import openai

# create your own openAI secret key
api_key = os.environ['API_KEY']

app = Flask(__name__)

openai.api_key = api_key

@app.route('/chat',methods=['POST'])
def chat_with_gpt():
    data = request.get_json()
    if 'message' not in data:
        return jsonify({'error':'Message parameter is missing'}), 400
    
    message = data['message']

    """ completion model choices:
        gpt-4-1106-preview
        gpt-3.5-turbo-1106
    """
    # response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt = message,
    #     max_tokens = 100
    # )
    # feedback = response.choices[0].text.strip()

    """fine-tuned models"""
    # ft:gpt-3.5-turbo-1106:university-of-chicago::8Nl21jbw -> trained on rating 1-5
    # ft:gpt-3.5-turbo-1106:personal::8Qi9Jant -> trained on rating 1-5 with more data
    # ft:gpt-3.5-turbo-1106:university-of-chicago::8YgELacB -> trained on rating 1-3 with more data
    completion = openai.ChatCompletion.create(model="ft:gpt-3.5-turbo-1106:university-of-chicago::8YgELacB",
                                              messages=[{"role": "user", "content": message}])
                                            #   temperature = 0.5)
    feedback = completion.choices[0].message.content
    return jsonify({'feedback':feedback})

if __name__ == '__main__':
    app.run(host='localhost',port=8443)
