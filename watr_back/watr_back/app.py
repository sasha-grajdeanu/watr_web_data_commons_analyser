from flask import Flask
from Classification.view import classification

app = Flask(__name__)
app.register_blueprint(classification, url_prefix='/api')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
