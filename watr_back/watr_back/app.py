import logging

from flask import Flask
from flask_cors import CORS

from watr_back.controllers.classification.classification_controller import classification
from watr_back.controllers.classification.classification_graph_controller import classificationGraph
from watr_back.controllers.classification.classification_stats_controller import classificationStats
from watr_back.controllers.classification.properties_controller import properties
from watr_back.handlers.error_handlers import error_handlers
from watr_back.middlewares.content_type_middleware import content_type_middleware

logging.basicConfig(
                level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')

app = Flask(__name__)
CORS(app)

content_type_middleware(app)
error_handlers(app)

app.register_blueprint(classification, url_prefix='/api')
app.register_blueprint(properties, url_prefix='/api')
app.register_blueprint(classificationGraph, url_prefix='/api')
app.register_blueprint(classificationStats, url_prefix='/api')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
