# ChatGPT Model

## Create your own OpenAI API key
Create your own API key from `https://platform.openai.com/account/api-keys`
Fill the `run_chatGPT_service.bat` with your own SECRET API KEY.

## Launch ChatGPT Service
- Execute `run_chatGPT_service.bat` to start your ChatGPT connection. 
- If successfully launched ChatGPT Service, you'll see the server ip and port number prompted in your terminal, e.g. * Running on http://10.0.0.8:8443/ 

## Start to predict news sentiments
- Execute `backtest.py` and set your file path. The file should contain a column of "corpora" waiting to be scored by ChatGPT.
- Successful execution will create another column "Score_by_ChatGPT" containing the prediction score by ChatGPT.
