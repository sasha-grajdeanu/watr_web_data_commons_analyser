import logging

from flask import Flask
from flask_cors import CORS

from flask_swagger_ui import get_swaggerui_blueprint

from controllers.alignment.alignment_data_controller import alignment
from controllers.alignment.alignment_html_controller import alignment_html
from controllers.alignment.alignment_json_ld_controller import alignment_json_ld
from controllers.alignment.alignment_statistics_controller import alignmentStats
from controllers.alignment.alignment_statistics_graph_controller import alignmentStatsGraph
from controllers.alignment.alignment_table_controller import alignmentTable
from controllers.classification.classification_data_controller import classification
from controllers.classification.classification_graph_controller import classificationGraph
from controllers.classification.classification_html_controller import classification_html
from controllers.classification.classification_json_ld_controller import classification_json_ld
from controllers.classification.classification_statistics_controller import classificationStats
from controllers.classification.classification_statistics_graph_controller import classificationStatsGraph
from controllers.classification.properties_controller import properties
from controllers.comparation.compare_data_controller import compare_data
from controllers.comparation.compare_download_statistics_controller import compare_download_statistics
from controllers.comparation.compare_html_controller import compare_html
from controllers.comparation.compare_json_ld_controller import compare_json_ld
from controllers.comparation.compare_statistics_controller import compare_statistics
from controllers.download_stats_controller import downloadStats
from controllers.visualisation.visualise__graph_controller import visualisation_graph
from controllers.visualisation.visualise_data_controller import visualisation_data
from controllers.visualisation.visualise_download_statistics import download_visualisation_statistics
from controllers.visualisation.visualise_statistics_controller import visualisation_statistics
from controllers.visualisation.visualize_html_controller import visualisation_html
from controllers.visualisation.visualize_json_controller import visualisation_json_ld
from handlers.error_handlers import error_handlers
from middlewares.content_type_middleware import content_type_middleware

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')
app = Flask(__name__)
CORS(app)

content_type_middleware(app)
error_handlers(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    }
)

app.register_blueprint(swaggerui_blueprint)


app.register_blueprint(visualisation_data, url_prefix='/api/visualise')
app.register_blueprint(visualisation_html, url_prefix='/api/visualise')
app.register_blueprint(visualisation_json_ld, url_prefix='/api/visualise')
app.register_blueprint(visualisation_graph, url_prefix='/api/visualise')
app.register_blueprint(visualisation_statistics, url_prefix='/api/visualise')
app.register_blueprint(download_visualisation_statistics, url_prefix='/api/visualise')

app.register_blueprint(compare_data, url_prefix='/api/compare')
app.register_blueprint(compare_html, url_prefix='/api/compare')
app.register_blueprint(compare_json_ld, url_prefix='/api/compare')
app.register_blueprint(compare_statistics, url_prefix='/api/compare')
app.register_blueprint(compare_download_statistics, url_prefix='/api/compare')

app.register_blueprint(properties, url_prefix='/api/classify')
app.register_blueprint(classification, url_prefix='/api/classify')
app.register_blueprint(classification_html, url_prefix='/api/classify')
app.register_blueprint(classification_json_ld, url_prefix='/api/classify')
app.register_blueprint(classificationGraph, url_prefix='/api/classify')
app.register_blueprint(classificationStats, url_prefix='/api/classify')
app.register_blueprint(classificationStatsGraph, url_prefix='/api/classify')

app.register_blueprint(alignment, url_prefix='/api/align')
app.register_blueprint(alignment_html, url_prefix='/api/align')
app.register_blueprint(alignment_json_ld, url_prefix='/api/align')
app.register_blueprint(alignmentTable, url_prefix='/api/align')
app.register_blueprint(alignmentStats, url_prefix='/api/align')
app.register_blueprint(alignmentStatsGraph, url_prefix='/api/align')

app.register_blueprint(downloadStats, url_prefix='/api')


@app.route('/api')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
