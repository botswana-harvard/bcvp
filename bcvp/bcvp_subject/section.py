from edc_dashboard.section import BaseSectionView, site_sections

from .search import CallSearchByWord
from .search import SubjectSearchByWord
from .models import SubjectEligibility


class SectionSubjectView(BaseSectionView):
    section_name = 'subject'
    section_display_name = 'Subject'
    section_display_index = 2
    section_template = 'section_subject.html'
    dashboard_url_name = 'subject_dashboard_url'
    add_model = SubjectEligibility
    search = {'word': SubjectSearchByWord}
    show_most_recent = True


class SectionCallView(BaseSectionView):
    section_name = 'call_manager'
    section_display_name = 'Call Manager'
    section_display_index = 1
    section_template = 'section_subject.html'
    dashboard_url_name = 'subject_dashboard_url'
#     add_model = Call
    search = {'word': CallSearchByWord}
    show_most_recent = True

site_sections.register(SectionSubjectView)
site_sections.register(SectionCallView)
