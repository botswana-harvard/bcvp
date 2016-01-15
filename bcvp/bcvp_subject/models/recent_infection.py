from django.db import models
from django.core.validators import RegexValidator

from edc_base.bw.validators import BWCellNumber
from edc_base.encrypted_fields import EncryptedCharField, EncryptedDecimalField, IdentityField


class RecentInfection(models.Model):

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        blank=True,
        db_index=True,
        unique=True)

    dob = models.DateField(
        verbose_name="Date of birth",
        null=True,
        blank=False,
        help_text="Format is YYYY-MM-DD")

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters '
                     'only in upper case, no spaces.'))],
        null=True)

    identity = IdentityField(
        null=True,
        blank=True)

    test_date = models.DateTimeField(
        verbose_name='Date / Time test was performed',
        null=True,
        blank=True,
        help_text=(
            'If not drawn, leave blank. Same as date and time of finger prick in case on DBS.'))

    specimen_identifier = models.CharField(
        verbose_name='Specimen Id',
        max_length=50,
        null=True,
        blank=True,
        editable=False,
        unique=True,)

    drawn_datetime = models.DateTimeField(
        verbose_name='Date / Time Specimen Drawn',
        null=True,
        blank=True,
        help_text=(
            'If not drawn, leave blank. Same as date and time of finger prick in case on DBS.'))

    result = models.CharField(
        verbose_name='Result',
        max_length=50,
        null=True,
        blank=True,
        help_text='')

    gps_lon = EncryptedDecimalField(
        verbose_name='longitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    gps_lat = EncryptedDecimalField(
        verbose_name='latitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    contact_cell_number = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,)

    alt_contact_cell_number = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number (alternate)",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,)

    objects = models.Manager()

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
