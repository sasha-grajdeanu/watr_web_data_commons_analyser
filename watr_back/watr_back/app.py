import logging
from controllers.visualisation.visualise_controller import visualisation
from controllers.visualisation.visualize_json_controller import visualisation_json_ld
from controllers.visualisation.visualize_html_controller import visualisation_html
from flask import Flask
from flask_cors import CORS

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')
app = Flask(__name__)
CORS(app)
app.register_blueprint(visualisation, url_prefix='/api')
app.register_blueprint(visualisation_json_ld, url_prefix='/api')
app.register_blueprint(visualisation_html, url_prefix='/api')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
