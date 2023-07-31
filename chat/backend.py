# Backend interface for the Jua Chat feature
import os
from flask import Flask
from flask import request
from flask_socketio import SocketIO
from flask_socketio import send, emit

os.environ["OPENAI_API_KEY"] = "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"

from paperqa import Docs
import pickle

docs = Docs()
app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins=["https://127.0.0.1:5173"])


def loadDocuments():
    # Loads the documents from the docs folder for all models of machine

    for root, dirs, files in os.walk("docs", topdown=False):
        for name in files:
            if not name.startswith("."):
                # Replace unimportant characters to clean up file name
                charsToReplace = ["-", "_", ".pdf"]
                citation = name
                for char in charsToReplace:
                    citation = citation.replace(char, " ")
                citation = citation.title()
                print(f"Loading document: {citation} (filename: {name})")
                docs.add(os.path.join(root, name), citation=citation, docname=citation)
        for name in dirs:
            print("New directory: ", os.path.join(root, name))


@socketio.on("json")
def query(json):
    print("receieved message, ", json)
    device = json["device"]
    query = json["query"]
    # Queries the model for a response
    # device: device the question is being asked for (eg: GE Logiq series)
    # query: the query to ask the model
    prompt = f"""
    Respond to the following question about a medical device: {query}.  
    Use terms that are easily understandable, even to those that may have limited knowledge of servicing
    and maintenace for medical devices. Prioritize SIMPLE, ACTIONABLE steps for troubleshooting. Avoid making vague statements if at all possible. If you do not have a specific answer to the problem, you may make inferences based on your knowledge of the device.
    The product the user is asking for support for is the {device}. Use as many specific details as possible from the product's documentation. DO NOT include specific details that pertains to another series of 
    products. For example, do not include specific information about a Siemens product when asked about a GE ultrasound machine.
    It is okay to provide very general advice based on other machines of the same type if you do not have any information about that product.
    Limit your responses to 3-4 sentences at a time, and NEVER respond with "I cannot answer" or similar statements. If you do not have an answer, you may respond with a question to the user to help them narrow down the problem. If a professional is required to fix the problem, please give an overview of what they would be required to do and what knowledge they might need so that the
    user can more effectively use it to find technicians on our platform.
    """
    response = docs.query(prompt, max_sources=3)

    print(
        f"""Question: {query}
           Answer: {response.answer}\n"""
    )

    send({"content": response.answer}, json=True)


def save():
    with open("docs.pkl", "wb") as f:
        pickle.dump(docs, f)


def load():
    with open("docs.pkl", "rb") as f:
        return pickle.load(f)


@socketio.on("connect")
def connect():
    print("Connected to client")


if os.path.isfile("docs.pkl") and input("Load pickle? (y/n)").lower() == "y":
    docs = load()
else:
    print("Reloading documents ...")
    loadDocuments()
    print("Saving pickle")
    save()

if __name__ == "__main__":
    socketio.run(app)
