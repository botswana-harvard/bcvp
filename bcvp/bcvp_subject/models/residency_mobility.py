from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_constants.constants import NOT_APPLICABLE
from edc_constants.choices import YES_NO
from edc_base.model.fields import OtherCharField

from bcvp.bcvp.choices import LENGTHRESIDENCE_CHOICE, NIGHTSAWAY_CHOICE, CATTLEPOSTLANDS_CHOICE

from .subject_crf_model import SubjectCrfModel


class ResidencyMobility(SubjectCrfModel):

    """A model completed by the user on the residency status of the participant."""

    length_residence = models.CharField(
        verbose_name='How long have you lived in this community?',
        max_length=25,
        choices=LENGTHRESIDENCE_CHOICE)

    permanent_resident = models.CharField(
        verbose_name="In the past 12 months, have you typically spent 14 or"
                     " more nights per month in this community? ",
        max_length=10,
        choices=YES_NO,
        help_text=("If participant has moved into the "
                   "community in the past 12 months, then "
                   "since moving in has the participant typically "
                   "spent more than 14 nights per month in this community. "
                   "If 'NO (or don't want to answer)' STOP. Participant cannot be enrolled."))

    intend_residency = models.CharField(
        verbose_name="Do you intend to move out of the community in the next 12 months?",
        max_length=25,
        choices=YES_NO)

    nights_away = models.CharField(
        verbose_name=(
            "In the past 12 months, in total how many nights did you spend away"
            " from this community, including visits to cattle post and lands?"
            "[If you don't know exactly, give your best guess]"),
        max_length=35,
        choices=NIGHTSAWAY_CHOICE)

    cattle_postlands = models.CharField(
        verbose_name=(
            "In the past 12 months, during the times you were away from this community, "
            "where were you primarily staying?"),
        max_length=25,
        choices=CATTLEPOSTLANDS_CHOICE,
        default=NOT_APPLICABLE)

    cattle_postlands_other = OtherCharField()

    history = AuditTrail()

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Residency & Mobility"
        verbose_name_plural = "Residency & Mobility"
