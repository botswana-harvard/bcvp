from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future
from edc_constants.choices import YES_NO, YES_NO_DWTA

from bcvp.bcvp.choices import (
    WHYNOARV_CHOICE, ADHERENCE4DAY_CHOICE, ADHERENCE4WK_CHOICE, NO_MEDICAL_CARE, WHYARVSTOP_CHOICE)

from .subject_crf_model import SubjectCrfModel


class HivCareAdherence(SubjectCrfModel):
    """A model completed by the user on the participant's access to and adherence to HIV care."""

    first_positive = models.DateField(
        verbose_name="When was your first positive HIV test result?",
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text=("Note: If participant does not want to answer, leave blank. "
                   "If participant is unable to estimate date, leave blank."))

    medical_care = models.CharField(
        verbose_name="Have you ever received HIV-related medical or clinical"
                     " care, for such things as a CD4 count (masole), IDCC/ PMTCT"
                     " registration, additional clinic-based counseling?",
        max_length=25,
        choices=YES_NO_DWTA,
        null=True,
        blank=True,
        help_text="if 'YES', answer HIV medical care section")

    no_medical_care = models.CharField(
        verbose_name="What is the main reason you have not received HIV-related"
                     " medical or clinical care?",
        max_length=70,
        null=True,
        blank=True,
        choices=NO_MEDICAL_CARE)

    no_medical_care_other = OtherCharField()

    ever_recommended_arv = models.CharField(
        verbose_name="Have you ever been recommended by a doctor/nurse or other healthcare "
                     "worker to start antiretroviral therapy (ARVs), a combination of medicines "
                     "to treat your HIV infection? [common medicines include: combivir, truvada, "
                     "atripla, nevirapine]",
        max_length=25,
        choices=YES_NO_DWTA,
        null=True,
        blank=True)

    ever_taken_arv = models.CharField(
        verbose_name="Have you ever taken any antiretroviral therapy (ARVs) for your HIV infection?"
                     " [For women: Do not include treatment that you took during pregnancy to protect "
                     "your baby from HIV]",
        max_length=25,
        choices=YES_NO_DWTA,
        null=True,
        blank=False)

    why_no_arv = models.CharField(
        verbose_name="What was the main reason why you have not started ARVs?",
        max_length=75,
        null=True,
        blank=True,
        choices=WHYNOARV_CHOICE)

    why_no_arv_other = OtherCharField()

    first_arv = models.DateField(
        verbose_name="When did you first start taking antiretroviral therapy (ARVs)?",
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text=("Note: If participant does not want to answer,leave blank.  "
                   "If participant is unable to estimate date, leave blank."))

    on_arv = models.CharField(
        verbose_name="Are you currently taking antiretroviral therapy (ARVs)?",
        max_length=25,
        choices=YES_NO_DWTA,
        null=True,
        blank=False,
        help_text="If yes, need to answer next two questions.")

    clinic_receiving_from = models.CharField(
        verbose_name='Which clinic facility are you already receiving therapy from?',
        default=None,
        null=True,
        blank=True,
        max_length=50)

    next_appointment_date = models.DateField(
        verbose_name="When is your next appointment at this facility?",
        default=None,
        null=True,
        blank=True)

    arv_stop_date = models.DateField(
        verbose_name="When did you stop taking ARV\'s?",
        validators=[date_not_future],  # Q15
        null=True,
        blank=True)

    arv_stop = models.CharField(
        verbose_name="What was the main reason why you stopped taking ARVs?",
        max_length=80,
        choices=WHYARVSTOP_CHOICE,
        null=True,
        blank=True)

    arv_stop_other = OtherCharField()

    adherence_4_day = models.CharField(
        verbose_name="During the past 4 days, on how many days have you missed taking all your"
                     " doses of antiretroviral therapy (ART)?",
        max_length=25,
        choices=ADHERENCE4DAY_CHOICE,
        null=True,
        blank=True)

    adherence_4_wk = models.CharField(
        verbose_name="Thinking about the past 4 weeks, on average, how would you rate your "
                     "ability to take all your medications as prescribed?",
        max_length=25,
        null=True,
        blank=True,
        choices=ADHERENCE4WK_CHOICE)

    arv_evidence = models.CharField(
        verbose_name="Is there evidence [OPD card, tablets, masa number] that the participant is on therapy?",
        choices=YES_NO,
        null=True,
        blank=True,
        max_length=3)

    history = AuditTrail()

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "HIV Care & Adherence"
        verbose_name_plural = "HIV Care & Adherence"
