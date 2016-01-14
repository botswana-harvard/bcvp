from edc_dashboard.section import BaseSectionView, site_sections

from .models import SubjectEligibility
from .search import SubjectSearchByWord


class SectionSubjectView(BaseSectionView):
    section_name = 'subject'
    section_display_name = 'Subject'
    section_display_index = 10
    section_template = 'section_subject.html'
    dashboard_url_name = 'subject_dashboard_url'
    add_model = SubjectEligibility
    search = {'word': SubjectSearchByWord}
    show_most_recent = True

site_sections.register(SectionSubjectView)
