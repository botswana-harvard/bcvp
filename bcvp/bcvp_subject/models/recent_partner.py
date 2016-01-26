from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_constants.choices import GENDER, POS_NEG_UNKNOWN
from edc_constants.choices import YES_NO_REFUSED, YES_NO_DONT_KNOW

from bcvp.bcvp.choices import (
    RELATIONSHIP_TYPE, MAIN_PARTNER_RESIDENCY, SEX_REGULARITY, INTERCOURSE_TYPE, DAY_MON_YEAR)

from .subject_crf_model import SubjectCrfModel


class RecentPartner(SubjectCrfModel):

    rel_type = models.CharField(
        verbose_name="What type of relationship do you have with this person?",
        max_length=37,
        choices=RELATIONSHIP_TYPE)

    rel_type_other = OtherCharField()

    partner_residency = models.CharField(
        verbose_name="To the best of your knowledge, where does you main sexual partner live?",
        max_length=25,
        choices=MAIN_PARTNER_RESIDENCY)

    partner_age = models.IntegerField(
        verbose_name="How old is this sexual partner?",
        max_length=2,
        help_text="If you don't know for sure, please give a best guess")

    partner_gender = models.CharField(
        verbose_name="Is this partner male or female? ",
        max_length=6,
        choices=GENDER)

    last_sex_contact = models.IntegerField(
        verbose_name="When was the last (most recent) time you had sex with"
                     " this person (how long ago)? ",
        max_length=2,
        help_text=('You can give either a date or the number of days/months/years since last sex. '
                   'Interviewer, convert to days and record'))

    last_sex_period = models.CharField(
        verbose_name="Record if number is in days/months/years",
        choices=DAY_MON_YEAR,
        max_length=6,
        blank=True,
        null=True,)

    first_sex_contact = models.IntegerField(
        verbose_name="When was the first time you had sex with this person (how long ago)? ",
        max_length=2,
        help_text=('You can give either a date or the number of days/months/years since last sex. '
                   'Interviewer, convert to days and record'))

    first_sex_period = models.CharField(
        verbose_name="Record if number is in days/months/years",
        choices=DAY_MON_YEAR,
        max_length=6,
        blank=True,
        null=True,)

    regular_sex = models.IntegerField(
        verbose_name="During the last 3 months (of your relationship if it has ended) how"
                     " many times a month (on average) did you have sex?",
        max_length=2)

    having_sex = models.CharField(
        verbose_name="Are you still having sex with this person? ",
        max_length=25,
        choices=YES_NO_REFUSED,
        null=True)

    having_sex_reg = models.CharField(
        verbose_name="Are you still having sex with this person? ",
        max_length=25,
        choices=SEX_REGULARITY,
        help_text="")

    alcohol_before_sex = models.CharField(
        verbose_name="Last time you had sex with this partner, did you drink alcohol before sex? ",
        max_length=20,
        choices=YES_NO_REFUSED)

    partner_status = models.CharField(
        verbose_name="Have you learned this partner's HIV status? ",
        max_length=8,
        choices=POS_NEG_UNKNOWN,
        help_text=" if 'HIV-negative or Don't know' go to question XX")

    partner_arv = models.CharField(
        verbose_name="Is this partner taking antiretroviral treatment?  ",
        max_length=15,
        null=True,
        blank=True,
        choices=YES_NO_DONT_KNOW)

    status_disclosure = models.CharField(
        verbose_name="Have you disclosed your HIV status to this partner? ",
        max_length=20,
        null=True,
        blank=True,
        choices=YES_NO_REFUSED)

    multiple_partners = models.CharField(
        verbose_name="To the best of your knowledge, did he/she ever have other"
                     " sex partners while you two were having a sexual relationship?",
        max_length=15,
        null=True,
        blank=True,
        choices=YES_NO_DONT_KNOW)

    intercourse_type = models.CharField(
        verbose_name="Can you tell me what type of sex you had with this sex partner?  ",
        max_length=25,
        null=True,
        blank=True,
        choices=INTERCOURSE_TYPE,
        help_text=("Remember: Vaginal sex is when a man puts his penis in the vagina of a woman."
                   " Anal sex is when a man puts his penis in the rectum of a man or a woman."))

    history = AuditTrail()

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Most Recent Partner"
        verbose_name_plural = "Most Recent Partner"
