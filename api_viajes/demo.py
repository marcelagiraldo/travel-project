from flask import Flask
app = Flask(__name__)
@app.route("/")
def greetings():
 return "Hello Backend developers!"
if __name__ == "__main__":
 app.run()
