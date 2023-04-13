from flask import Flask, render_template
from scripts.MEM import MEMM

app = Flask(__name__)

classifier = MEMM()
classifier.load_model()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/query/<string:sentence>')
def query(sentence):
    sentence = sentence.replace("%20", " ")
    words = sentence.strip().replace(".", "").split(" ")
    pdists = classifier.predict(sentence)

    return render_template('query.html', sentence=sentence, words=words, pdists=pdists)

if __name__ == "__main__":
    app.run(debug=True)


# DEBUG
# Chrome - Local webserver access denied
# Fix: GOTO chrome://net-internals/#sockets and flush socket pools
# chrome://net-internals/#sockets