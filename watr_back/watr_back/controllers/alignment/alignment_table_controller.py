from flask import Blueprint, jsonify

from watr_back.controllers.alignment.alignment_controller import align as controller_align
from watr_back.services.alignment.alignment_table_service import \
    get_alignment_table as service_get_alignment_table


alignmentTable = Blueprint('alignmentTable', __name__)

@alignmentTable.route('/align/table', methods=['POST'])
def align_table():
    align_data = controller_align()
    results = service_get_alignment_table(align_data)
    print("*"*80)
    print(results)
    return jsonify({"results": results})