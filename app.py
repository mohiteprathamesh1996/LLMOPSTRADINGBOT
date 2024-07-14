from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
from tradingbot.data_retrieval import generation
from tradingbot.data_ingestion import ingestdata

app = Flask(__name__)

load_dotenv()

vstore,inserted_ids=ingestdata(status=None)
chain=generation(vstore)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    result=chain.invoke(input)
    print("Response : ", result)
    return str(result)

if __name__ == '__main__':
    app.run(debug= True)