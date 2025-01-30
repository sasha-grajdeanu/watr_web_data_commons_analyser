from flask import Blueprint, jsonify

from controllers.alignment.alignment_controller import align as controller_align
from services.alignment.alignment_table_service import \
    get_alignment_table as service_get_alignment_table


alignmentTable = Blueprint('alignmentTable', __name__)

@alignmentTable.route('/align/table', methods=['GET'])
def align_table():
    align_data = controller_align()
    results = service_get_alignment_table(align_data)
    return jsonify({"results": results})