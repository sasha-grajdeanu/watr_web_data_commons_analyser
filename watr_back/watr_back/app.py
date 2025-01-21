import logging

from flask import Flask
from flask_cors import CORS


logging.basicConfig(
                level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')
app = Flask(__name__)
CORS(app)




@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
