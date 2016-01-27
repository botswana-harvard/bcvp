import urllib2
import json
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db import models
from django.core.validators import RegexValidator

from edc_base.audit_trail import AuditTrail
from edc_base.bw.validators import BWCellNumber
from edc_base.encrypted_fields import EncryptedCharField, IdentityField, FirstnameField
from edc_base.model.models import BaseUuidModel
from edc_registration.models import RegisteredSubject
from edc_map.classes import Mapper
from edc_map.classes import site_mappers
from edc_map.models import MapperMixin


from ..managers import RecentInfectionManager


class RecentInfection(MapperMixin, BaseUuidModel):

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

    objects = RecentInfectionManager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        # TODO: Make this URL generated not hard coded.
        if not self.id:
            try:
                RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
                raise ValidationError('Recent infection record for "{}" already exists.'.format(self.subject_identifier))
            except RegisteredSubject.DoesNotExist:
                # By leaving dob, initials and identity blank, then you are directing the application to pull from the
                # mpp system by REST, otherwise the application will use the provided data.
                if not self.dob and not self.initials and not self.identity:
                    url = 'http://localhost:8012/bhp_sync/{}/{}/?format=json&limit=5&subject_identifier={}'.format(
                        'api_cn',
                        'subjectconsent',
                        self.subject_identifier)
                    consent_json = self.pull_rest_json(url)
                    self.drawn_datetime = datetime.now()
                    self.subject_identifier = consent_json['objects'][0]['subject_identifier']
                    self.first_name = consent_json['objects'][0]['first_name']
                    self.dob = datetime.strptime(consent_json['objects'][0]['dob'], '%Y-%m-%d').date()
                    self.identity = consent_json['objects'][0]['identity']
                    self.initials = consent_json['objects'][0]['initials']
                    self.specimen_identifier = consent_json['objects'][0]['subject_identifier']
                    url = 'http://localhost:8012/bhp_sync/{}/{}/?format=json&limit=5&subject_identifier={}'.format(
                        'api_lc',
                        'locator',
                        self.subject_identifier)
                    locator_json = self.pull_rest_json(url)
                    self.subject_cell = locator_json['objects'][0]['subject_prefered_cell']
                    self.subject_cell_alt = locator_json['objects'][0]['kin_cell']
                    url = 'http://localhost:8012/bhp_sync/{}/{}/?format=json&limit=5&subject_identifier={}'.format(
                        'api_hd',
                        'household',
                        self.subject_identifier)
                    household_json = self.pull_rest_json(url)
                    lat, lon = self.covert_coordinates(household_json['objects'][0]['gps_point_1'],
                                                       household_json['objects'][0]['gps_point_11'],
                                                       household_json['objects'][0]['gps_point_2'],
                                                       household_json['objects'][0]['gps_point_21'])
                    self.gps_target_lat = lat
                    self.gps_target_lon = lon
        super(RecentInfection, self).save(*args, **kwargs)

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

    def natural_key(self):
        """Returns a natural key."""
        return (self.subject_identifier, ) + self.registered_subject.natural_key()

    @property
    def img_url(self):
        """Return the url to an image."""
        mapper = site_mappers.get_mapper(self.area_name)
        return mapper.image_file_url(self.pk)

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

    def pull_rest_json(self, url):
        try:
            req = urllib2.Request(url=url)
        except urllib2.URLError:
            raise
        try:
            f = urllib2.urlopen(req)
            response = f.read()
            json_response = json.loads(response)
        except urllib2.HTTPError:
            raise
        return json_response

    def covert_coordinates(self, south_deg, soth_mnts, east_deg, east_mnts):
        mapper = Mapper()
        lat = mapper.gps_lat(south_deg, soth_mnts)
        lon = mapper.gps_lon(east_deg, east_mnts)
        return (lat, lon)

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = 'Recent Infection'
        unique_together = ('dob', 'initials', 'identity', )
