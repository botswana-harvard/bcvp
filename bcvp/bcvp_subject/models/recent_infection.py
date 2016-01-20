from django.db import models
from django.core.validators import RegexValidator

from edc_base.audit_trail import AuditTrail
from edc_base.bw.validators import BWCellNumber
from edc_base.encrypted_fields import EncryptedCharField, EncryptedDecimalField, IdentityField, FirstnameField
from edc_base.model.models import BaseUuidModel
from edc_registration.models import RegisteredSubject


class RecentInfection(BaseUuidModel):

    """A model pre-populated with a list of potential participants."""

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        db_index=True,
        unique=True)

    first_name = FirstnameField()

    dob = models.DateField(
        verbose_name="Date of birth",
        help_text="Format is YYYY-MM-DD")

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters '
                     'only in upper case, no spaces.'))])

    identity = IdentityField(unique=True)

    test_date = models.DateTimeField(
        verbose_name='Date / Time test was performed',
        blank=True,
        null=True,
        help_text=(
            'If not drawn, leave blank. Same as date and time of finger prick in case on DBS.'))

    specimen_identifier = models.CharField(
        verbose_name='Specimen Id',
        max_length=50,
        unique=True)

    drawn_datetime = models.DateTimeField(
        verbose_name='Date / Time Specimen Drawn',
        blank=True,
        null=True,
        help_text=(
            'If not drawn, leave blank. Same as date and time of finger prick in case on DBS.'))

    result = models.CharField(
        verbose_name='Result',
        max_length=50,
        blank=True,
        null=True)

    gps_lon = EncryptedDecimalField(
        verbose_name='longitude',
        max_digits=10,
        blank=True,
        null=True,
        decimal_places=6)

    gps_lat = EncryptedDecimalField(
        verbose_name='latitude',
        max_digits=10,
        blank=True,
        null=True,
        decimal_places=6)

    subject_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number",
        validators=[BWCellNumber, ],
        blank=True,
        null=True,)

    subject_cell_alt = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number (alternate)",
        validators=[BWCellNumber, ],
        blank=True,
        null=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return self.subject_identifier

    @property
    def cell(self):
        return self.contact_cell_number

    @property
    def cell_alt(self):
        return self.alt_contact_cell_number

    @property
    def born(self):
        return self.dob.strftime('%Y-%m-%d')

    @property
    def report_datetime(self):
        return self.drawn_datetime

    @property
    def eligibility_matching_dict(self):
        eligibility_matching_attr = {}
        eligibility_matching_attr['dob'] = self.dob
        eligibility_matching_attr['initials'] = self.initials
        eligibility_matching_attr['identity'] = self.identity
        return eligibility_matching_attr

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = 'Recent Infection'
        unique_together = ('dob', 'initials', 'identity', )
