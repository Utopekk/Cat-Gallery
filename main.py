import requests
from flask import Flask, render_template_string, request,render_template,session,redirect


app = Flask(__name__)
app.secret_key = 'key'

API_KEY = ""


@app.route('/')
def home():
    response = requests.get(
        "https://api.thecatapi.com/v1/images/search",
        headers={"x-api-key": API_KEY}
    )

    data = response.json()
    image_url = data[0]["url"]
    return render_template('index.html', image_url=image_url)


@app.route("/like", methods=["POST"])
def like():
    liked_image_url = request.form["image_url"]

    if "liked_cats" not in session:
        session["liked_cats"] = []

    if liked_image_url not in session["liked_cats"]:
        session["liked_cats"].append(liked_image_url)
        session.modified = True

    return '', 204

@app.route("/gallery")
def gallery():
    liked_cats = session.get("liked_cats", [])
    return render_template('gallery.html', liked_cats=liked_cats)

if __name__ == "__main__":
    app.run(debug=True)
