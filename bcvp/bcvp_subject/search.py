from django.db.models import Q

from edc_dashboard.search import BaseSearchByWord

from .models import BcvpCall


class CallSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = BcvpCall
    order_by = ['-modified']
    template = 'call_manager_include.html'

    @property
    def qset(self):
        qset = (
            Q(subject_identifier__icontains=self.search_value) |
            Q(first_name__icontains=self.search_value) |
            Q(call_status__icontains=self.search_value) |
            Q(registered_subject__identity__icontains=self.search_value) |
            Q(registered_subject__first_name__icontains=self.search_value))
        return qset
