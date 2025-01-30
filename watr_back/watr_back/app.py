import logging
from flask import Flask
from flask_cors import CORS

from controllers.alignment.alignment_controller import alignment
from controllers.alignment.alignment_stats_controller import alignmentStats
from controllers.alignment.alignment_table_controller import alignmentTable
from controllers.classification.classification_controller import classification
from controllers.classification.classification_graph_controller import classificationGraph
from controllers.classification.classification_stats_controller import classificationStats
from controllers.classification.properties_controller import properties
from controllers.download_stats_controller import downloadStats
from handlers.error_handlers import error_handlers
from middlewares.content_type_middleware import content_type_middleware
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

content_type_middleware(app)
error_handlers(app)

app.register_blueprint(properties, url_prefix='/api')


app.register_blueprint(classification, url_prefix='/api')
app.register_blueprint(classificationGraph, url_prefix='/api')
app.register_blueprint(classificationStats, url_prefix='/api')


app.register_blueprint(alignment, url_prefix='/api')
app.register_blueprint(alignmentTable, url_prefix='/api')
app.register_blueprint(alignmentStats, url_prefix='/api')


app.register_blueprint(downloadStats, url_prefix='/api')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
