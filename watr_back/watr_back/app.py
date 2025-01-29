import logging

from controllers.comparation.compare_statistics_controller import compare_statistics
from controllers.visualisation.visualise__graph_controller import visualisation_graph
from controllers.visualisation.visualize_json_controller import visualisation_json_ld
from controllers.visualisation.visualize_html_controller import visualisation_html
from controllers.visualisation.visualise_statistics_controller import visualisation_statistics
from controllers.visualisation.visualise_download_statistics import download_visualisation_statistics
from controllers.comparation.compare_data_controller import compare_data
from controllers.comparation.compare_json_ld_controller import compare_json_ld
from controllers.comparation.compare_html_controller import compare_html
from controllers.comparation.compare_download_statistics_controller import compare_download_statistics
from flask import Flask
from flask_cors import CORS

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')
app = Flask(__name__)
CORS(app)
app.register_blueprint(visualisation_graph, url_prefix='/api/visualise')
app.register_blueprint(visualisation_json_ld, url_prefix='/api/visualise')
app.register_blueprint(visualisation_html, url_prefix='/api/visualise')
app.register_blueprint(visualisation_statistics, url_prefix='/api/visualise')
app.register_blueprint(download_visualisation_statistics, url_prefix='/api/visualise')

app.register_blueprint(compare_data, url_prefix='/api/compare')
app.register_blueprint(compare_json_ld, url_prefix='/api/compare')
app.register_blueprint(compare_html, url_prefix='/api/compare')
app.register_blueprint(compare_statistics, url_prefix='/api/compare')
app.register_blueprint(compare_download_statistics, url_prefix='/api/compare')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
