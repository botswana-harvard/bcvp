from collections import namedtuple

from edc_dashboard.section import BaseSectionView, site_sections

ModelMeta = namedtuple('ModelMeta', 'app_label model_name')


class SectionAdministrationView(BaseSectionView):
    section_name = 'administration'
    section_display_name = 'Administration'
    section_display_index = 140
    section_template = 'bcvp_section_administration.html'

    def contribute_to_context(self, context, request, *args, **kwargs):
        context.update({
            'subject_meta': ModelMeta('bcvp_subject', 'subject_consent'),
            'aliquot_type_meta': ModelMeta('bcvp_lab', 'aliquot_type'),
            'aliquot_meta': ModelMeta('bcvp_lab', 'aliquot'),
        })

site_sections.register(SectionAdministrationView, replaces='administration')
