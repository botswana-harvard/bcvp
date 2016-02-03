from edc_constants.constants import YES, UNKEYED, NOT_REQUIRED
from edc_rule_groups.classes import RuleGroup, site_rule_groups, Logic, CrfRule

from .models import SexualBehaviour, SubjectVisit


class RecentPartnerRuleGroup(RuleGroup):

    is_srh_referral = CrfRule(
        logic=Logic(
            predicate=('recent_partner', 'equals', YES),
            consequence=UNKEYED,
            alternative=NOT_REQUIRED),
        target_model=['recentpartner'])

    class Meta:
        app_label = 'bcvp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = SexualBehaviour

site_rule_groups.register(RecentPartnerRuleGroup)
