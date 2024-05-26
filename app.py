from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

with open("translate.json", encoding="utf-8") as file:
    intents = json.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_message = data.get("message")
    user_language = data.get("lang", "en")
    response = find_response(user_message, user_language)
    return jsonify({"response": response})


def find_response(message, lang):
    for intent in intents["intents"]:
        if message in intent["patterns"].get(lang, []):
            return intent["responses"].get(lang, ["Sorry, I don't understand that."])[0]
    default_responses = {
        "en": "Sorry, I don't understand that.",
        "ja": "すみません、それが理解できません。",
        "ta": "மன்னிக்கவும், நான் அதை புரிந்துகொள்ளவில்லை.",
    }

    return default_responses.get(lang, default_responses["en"])


if __name__ == "__main__":
    app.run(debug=True, port=6001)
