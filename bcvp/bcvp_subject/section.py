from edc_dashboard.section import BaseSectionView, site_sections

from .search import CallSearchByWord


class SectionCallView(BaseSectionView):
    section_name = 'call_manager'
    section_display_name = 'Participants'
    section_display_index = 1
    section_template = 'section_subject.html'
    dashboard_url_name = 'subject_dashboard_url'
#     add_model = Call
    search = {'word': CallSearchByWord}
    show_most_recent = True

site_sections.register(SectionCallView)
