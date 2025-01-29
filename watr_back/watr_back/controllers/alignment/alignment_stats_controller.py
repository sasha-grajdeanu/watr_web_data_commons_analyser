from flask import Blueprint

from watr_back.controllers.alignment.alignment_controller import align as controller_align
from watr_back.services.alignment.alignment_stats_service import \
    get_alignment_stats as service_get_alignment_stats

alignmentStats = Blueprint('alignmentStats', __name__)

@alignmentStats.route('align/stats', methods=['GET'])
def alignment_stats():
    align_data = controller_align()
    results = service_get_alignment_stats(align_data)
    return results