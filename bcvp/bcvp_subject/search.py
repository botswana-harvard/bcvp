from django.db.models import Q

from edc_dashboard.search import BaseSearchByWord

from .models import SubjectEligibility


class SubjectSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = SubjectEligibility
    order_by = ['-created']
    template = 'subjecteligibility_include.html'

    @property
    def qset(self):
        qset = (
            Q(registered_subject__subject_identifier__icontains=self.search_value) |
            Q(registered_subject__first_name__icontains=self.search_value))
        return qset