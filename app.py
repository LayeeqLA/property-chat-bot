from flask import Flask, render_template, request
import replicate

app = Flask(__name__)

def get_completion(prompt, model="gpt-3.5-turbo"):
    res = ''
    for event in replicate.stream(
    "meta/meta-llama-3-70b-instruct",
    input={
        "top_k": 50,
        "top_p": 0.9,
        "prompt": prompt,
        "max_tokens": 512,
        "min_tokens": 0,
        "temperature": 0.6,
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
        "presence_penalty": 1.15,
        "frequency_penalty": 0.2
    },
    ):
        res = res + ' ' + str(event)
    return res

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')  
    response = get_completion(userText)  
    #return str(bot.get_response(userText)) 
    return response
if __name__ == "__main__":
    app.run()