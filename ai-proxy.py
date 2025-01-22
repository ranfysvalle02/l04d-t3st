from flask import Flask, jsonify, request  
import os  
from openai import AzureOpenAI  
from dotenv import load_dotenv  
  
# Load the .env file  
load_dotenv()  
  
app = Flask(__name__)  
  
@app.route('/', methods=['GET'])  
def chat():  
    # Get the user query from the query parameters, default to "testing"  
    user_query = request.args.get('query', default='testing', type=str)  
  
    AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")  
    AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")  
  
    client = AzureOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT, api_version="2023-07-01-preview", api_key=AZURE_OPENAI_API_KEY)  
  
    chat_completion = client.chat.completions.create(  
        messages=[  
            {  
                "role": "user",  
                "content": user_query,  
            }  
        ],  
        model="gpt-4o",  
    )  
  
    return jsonify({  
        "chat_completion": chat_completion.choices[0].message.content  
    })  
  
if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=1020)  
