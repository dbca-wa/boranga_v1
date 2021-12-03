from boranga.components.organisations.models import Organisation
from reversion_compare.views import HistoryCompareDetailView


class OrganisationHistoryCompareView(HistoryCompareDetailView):
    """
    View for reversion_compare
    """
    model = Organisation
    template_name = 'boranga/reversion_history.html'
