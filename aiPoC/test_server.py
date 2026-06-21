from flask import Flask
import markdown2
app = Flask(__name__)

@app.route("/")
def hello():
    return markdown2.markdown(""" <lol@/ //id="pwn"//onclick="alert(1)"//**abc** """, safe_mode = True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
