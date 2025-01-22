from flask import Flask, jsonify, request  
import os  
from openai import AzureOpenAI  
from dotenv import load_dotenv  

# 3,740 tokens --> let's push the limits here
SAMPLE_CONTEXT = """
a8Jk2LmN5oPqRs9TuVwXyZ0AbC3dEfGh4IjKlMn5OpQr6StUv7WxYz8AbC9dEfG0hIjK1lMn2OpQ3rSt4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5Ab6Cd7Ef8Gh9Ij0Kl1Mn2Op3Qr4St5Uv6Wx7Yz8Ab9Cd0Ef1Gh2Ij3Kl4Mn5Op6Qr7St8Uv9Wx0Yz1Ab2Cd3Ef4Gh5Ij6Kl7Mn8Op9Qr0St1Uv2Wx3Yz4Ab5Cd6Ef7Gh8Ij9Kl0Mn1Op2Qr3St4Uv5Wx6Yz7Ab8Cd9Ef0Gh1Ij2Kl3Mn4Op5Qr6St7Uv8Wx9Yz0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St0Uv1Wx2Yz3Ab4Cd5Ef6Gh7Ij8Kl9Mn0Op1Qr2St3Uv4Wx5Yz6Ab7Cd8Ef9Gh0Ij1Kl2Mn3Op4Qr5St6Uv7Wx8Yz9Ab0Cd1Ef2Gh3Ij4Kl5Mn6Op7Qr8St9Uv0Wx1Yz2Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4Yz5
"""

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
    
    chat_completion = None
    def create_chat_completion(client, user_query, sample_context, model="gpt-4o"):
        try:
            return client.chat.completions.create(  
                messages=[  
                    {  
                        "role": "user",  
                        "content": user_query,  
                    },
                    {
                        "role":"user",
                        "content":f"""
                        {sample_context}
                        """
                    }  
                ],  
                model=model,  
            )
        except Exception as e:
            error_message = str(e)
            if "https://aka.ms/oai/quotaincrease" in error_message or "429" in error_message:
                print(f"Error with model {model}: {error_message}")
                if model == "gpt-4o":
                    print("Switching to gpt-35-turbo...")
                    return create_chat_completion(client, user_query, sample_context, model="gpt-35-turbo")
                else:
                    print("We tried so hard, and got so far - but in the end... it doesn't even matter.")
                    return None
                    # round robin?
                    #print("Switching to gpt-4o...")
                    #return create_chat_completion(client, user_query, sample_context, model="gpt-4o")
            else:
                print(f"An error occurred: {error_message}")
                return None

    chat_completion = create_chat_completion(client, user_query, SAMPLE_CONTEXT)
  
    return jsonify({  
        "chat_completion": chat_completion.choices[0].message.content  
    })  
  
if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=1020)  
