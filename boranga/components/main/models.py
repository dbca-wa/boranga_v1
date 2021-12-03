from __future__ import unicode_literals
import os

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
#from ledger.accounts.models import EmailUser, Document, RevisionedMixin
from ledger.accounts.models import EmailUser, RevisionedMixin
from django.contrib.postgres.fields.jsonb import JSONField


@python_2_unicode_compatible
class Region(models.Model):
    name = models.CharField(max_length=200, unique=True)
    forest_region = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        app_label = 'boranga'

    def __str__(self):
        return self.name

    # @property
    # def districts(self):
    #     return District.objects.filter(region=self)


@python_2_unicode_compatible
class District(models.Model):
    region = models.ForeignKey(Region, related_name='districts')
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=3)
    archive_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        app_label = 'boranga'

    def __str__(self):
        return self.name

    @property
    def parks(self):
        return Parks.objects.filter(district=self)

    @property
    def land_parks(self):
        return Park.objects.filter(district=self, park_type='land')

    @property
    def land_parks_external(self):
        return Park.objects.filter(district=self, park_type='land').exclude(visible_to_external=False)

    @property
    def marine_parks(self):
        return Park.objects.filter(district=self, park_type='marine')

    @property
    def marine_parks_external(self):
        return Park.objects.filter(district=self, park_type='marine').exclude(visible_to_external=False)



@python_2_unicode_compatible
class AccessType(models.Model):
    name = models.CharField(max_length=200, blank=True)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        app_label = 'boranga'

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class ActivityType(models.Model):
    ACTIVITY_TYPE_CHOICES = (
        ('land', 'Land'),
        ('marine', 'Marine'),
        ('Film', 'Film'),
    )
    type_name = models.CharField('Activity Type', max_length=40, choices=ACTIVITY_TYPE_CHOICES,
                                        default=ACTIVITY_TYPE_CHOICES[0][0])
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['type_name']
        app_label = 'boranga'

    def __str__(self):
        return self.type_name

@python_2_unicode_compatible
class ActivityCategory(models.Model):
    ACTIVITY_TYPE_CHOICES = (
        ('land', 'Land'),
        ('marine', 'Marine'),
        ('Film', 'Film'),
        ('event', 'Event'),
    )
    name = models.CharField(max_length=200, blank=True)
    visible = models.BooleanField(default=True)
    activity_type = models.CharField('Activity Type', max_length=40, choices=ACTIVITY_TYPE_CHOICES,
                                        default=ACTIVITY_TYPE_CHOICES[0][0])

    class Meta:
        ordering = ['name']
        app_label = 'boranga'
        verbose_name_plural= 'Activity Categories'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Activity(models.Model):
    name = models.CharField(max_length=200, blank=True)
    visible = models.BooleanField(default=True)
    activity_category = models.ForeignKey(ActivityCategory, related_name='activities')

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Activities"
        app_label = 'boranga'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Park(models.Model):
    PARK_TYPE_CHOICES = (
        ('land', 'Land'),
        ('marine', 'Marine'),
        ('Film', 'Film'),
    )
    district = models.ForeignKey(District, related_name='parks')
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=10, blank=True)
    park_type = models.CharField('Park Type', max_length=40, choices=PARK_TYPE_CHOICES,
                                        default=PARK_TYPE_CHOICES[0][0])
    allowed_activities = models.ManyToManyField(Activity, blank=True)
    allowed_access = models.ManyToManyField(AccessType, blank=True)

    adult_price = models.DecimalField('Adult (price per adult)', max_digits=5, decimal_places=2)
    child_price = models.DecimalField('Child (price per child)', max_digits=5, decimal_places=2)
    #oracle_code = models.CharField(max_length=50)

    # editable=False --> related to invoice PDF generation, currently GST is computed assuming GST is payable for ALL parks.
    # Must fix invoice calc. GST per park in pdf line_items, for net GST if editable is to be set to True
    is_gst_exempt = models.BooleanField(default=False, editable=False)
    visible_to_external= models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        app_label = 'boranga'
        #unique_together = ('id', 'proposal',)

    def __str__(self):
        return self.name

    @property
    def allowed_activities_ids(self):
        return [i.id for i in self.allowed_activities.all()]

    @property
    def allowed_access_ids(self):
        return [i.id for i in self.allowed_access.all()]

    @property
    def zone_ids(self):
        return [i.id for i in self.zones.all()]

    def oracle_code(self, application_type):
        """ application_type - TClass/Filming/Event """
        try:
            return self.oracle_codes.get(code_type=application_type).code
        except:
            raise ValidationError('Unknown application type: {}'.format(application_type))


@python_2_unicode_compatible
class Zone(models.Model):
    name = models.CharField(max_length=200, blank=True)
    visible = models.BooleanField(default=True)
    park = models.ForeignKey(Park, related_name='zones')
    allowed_activities = models.ManyToManyField(Activity, blank=True)


    class Meta:
        ordering = ['name']
        app_label = 'boranga'

    def __str__(self):
        return self.name

    @property
    def allowed_activities_ids(self):
        return [i.id for i in self.allowed_activities.all()]



@python_2_unicode_compatible
class Trail(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=10, blank=True)
    allowed_activities = models.ManyToManyField(Activity, blank=True)

    class Meta:
        ordering = ['name']
        app_label = 'boranga'
        #unique_together = ('id', 'proposal',)

    def __str__(self):
        return self.name

    @property
    def section_ids(self):
        return [i.id for i in self.sections.all()]

    @property
    def allowed_activities_ids(self):
        return [i.id for i in self.allowed_activities.all()]

@python_2_unicode_compatible
class Section(models.Model):
    name = models.CharField(max_length=200, blank=True)
    visible = models.BooleanField(default=True)
    trail = models.ForeignKey(Trail, related_name='sections')
    doc_url= models.CharField('Document URL',max_length=255, blank=True)

    class Meta:
        ordering = ['name']
        app_label = 'boranga'

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class RequiredDocument(models.Model):
    question = models.TextField(blank=False)
    activity = models.ForeignKey(Activity,null=True, blank=True)
    park= models.ForeignKey(Park,null=True, blank=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return self.question

@python_2_unicode_compatible
class ApplicationType(models.Model):
    """
    for park in Park.objects.all().order_by('id'):
        ParkPrice.objects.create(park=park, adult=10.0, child=7.50, senior=5.00)
    """
    #TCLASS = 'T Class'
    TCLASS = 'Commercial operations'
    ECLASS = 'E Class'
    FILMING = 'Filming'
    EVENT = 'Event'
    name = models.CharField(max_length=64, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    visible = models.BooleanField(default=True)

    application_fee = models.DecimalField('Application Fee', max_digits=6, decimal_places=2, null=True)
    oracle_code_application = models.CharField(max_length=50)
    oracle_code_licence = models.CharField(max_length=50)
    is_gst_exempt = models.BooleanField(default=True)

    # Events
    events_park_fee = models.DecimalField('Events Park Fee (per participant, per park)', max_digits=6, decimal_places=2, default=0.0)

    # filming
    filming_fee_half_day = models.DecimalField('Filming half day fee', max_digits=6, decimal_places=2, default=0.0)
    filming_fee_full_day = models.DecimalField('Filming full day fee', max_digits=6, decimal_places=2, default=0.0)
    filming_fee_2days = models.DecimalField('Filming two days fee', max_digits=6, decimal_places=2, default=0.0)
    filming_fee_3days = models.DecimalField('Filming 3 days or more fee', max_digits=6, decimal_places=2, default=0.0)

    photography_fee_half_day = models.DecimalField('Photography half day fee', max_digits=6, decimal_places=2, default=0.0)
    photography_fee_full_day = models.DecimalField('Photography full day fee', max_digits=6, decimal_places=2, default=0.0)
    photography_fee_2days = models.DecimalField('Photography two days fee', max_digits=6, decimal_places=2, default=0.0)
    photography_fee_3days = models.DecimalField('Photography 3 days or more fee', max_digits=6, decimal_places=2, default=0.0)

    # T Class
    max_renewals = models.PositiveSmallIntegerField('Maximum number of times an Approval can be renewed', null=True, blank=True)
    max_renewal_period = models.PositiveSmallIntegerField('Maximum period of each Approval renewal (Years)', null=True, blank=True)
    licence_fee_2mth = models.DecimalField('T Class Licence Fee (2 Months)', max_digits=6, decimal_places=2, default=0.0)
    licence_fee_1yr = models.DecimalField('T Class Licence Fee (1 Year)', max_digits=6, decimal_places=2, default=0.0)

    class Meta:
        ordering = ['order', 'name']
        app_label = 'boranga'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class OracleCode(models.Model):
    CODE_TYPE_CHOICES = (
        (ApplicationType.TCLASS, ApplicationType.TCLASS),
        (ApplicationType.FILMING, ApplicationType.FILMING),
        (ApplicationType.EVENT, ApplicationType.EVENT),
    )
    park = models.ForeignKey(Park, related_name='oracle_codes')
    code_type = models.CharField('Application Type', max_length=64, choices=CODE_TYPE_CHOICES,
                                        default=CODE_TYPE_CHOICES[0][0])
    code = models.CharField(max_length=50, blank=True)
    archive_date = models.DateField(null=True, blank=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return '{} - {}'.format(self.code_type, self.code)


@python_2_unicode_compatible
class ActivityMatrix(models.Model):
    name = models.CharField(verbose_name='Activity matrix name', max_length=24, choices=[('Commercial Operator', u'Commercial Operator')], default='Commercial Operator')
    description = models.CharField(max_length=256, blank=True, null=True)
    schema = JSONField()
    replaced_by = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    version = models.SmallIntegerField(default=1, blank=False, null=False)
    ordered = models.BooleanField('Activities Ordered Alphabetically', default=False)

    class Meta:
        app_label = 'boranga'
        unique_together = ('name', 'version')
        verbose_name_plural = "Activity matrix"

    def __str__(self):
        return '{} - v{}'.format(self.name, self.version)


@python_2_unicode_compatible
class Tenure(models.Model):
    name = models.CharField(max_length=255, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    application_type = models.ForeignKey(ApplicationType, related_name='tenure_app_types')

    class Meta:
        ordering = ['order', 'name']
        app_label = 'boranga'

    def __str__(self):
        return '{}: {}'.format(self.name, self.application_type)

@python_2_unicode_compatible
class Question(models.Model):
    CORRECT_ANSWER_CHOICES = (
        ('answer_one', 'Answer one'), ('answer_two', 'Answer two'), ('answer_three', 'Answer three'),
        ('answer_four', 'Answer four'))
    question_text = models.TextField(blank=False)
    answer_one = models.CharField(max_length=200, blank=True)
    answer_two = models.CharField(max_length=200, blank=True)
    answer_three = models.CharField(max_length=200, blank=True)
    answer_four = models.CharField(max_length=200, blank=True)
    #answer_five = models.CharField(max_length=200, blank=True)
    correct_answer = models.CharField('Correct Answer', max_length=40, choices=CORRECT_ANSWER_CHOICES,
                                       default=CORRECT_ANSWER_CHOICES[0][0])
    application_type = models.ForeignKey(ApplicationType, null=True, blank=True)

    class Meta:
        #ordering = ['name']
        app_label = 'boranga'

    def __str__(self):
        return self.question_text

    @property
    def correct_answer_value(self):
        return getattr(self, self.correct_answer)


@python_2_unicode_compatible
class UserAction(models.Model):
    who = models.ForeignKey(EmailUser, null=False, blank=False)
    when = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    what = models.TextField(blank=False)

    def __str__(self):
        return "{what} ({who} at {when})".format(
            what=self.what,
            who=self.who,
            when=self.when
        )

    class Meta:
        abstract = True
        app_label = 'boranga'


class CommunicationsLogEntry(models.Model):
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone Call'),
        ('mail', 'Mail'),
        ('person', 'In Person'),
        ('onhold', 'On Hold'),
        ('onhold_remove', 'Remove On Hold'),
        ('with_qaofficer', 'With QA Officer'),
        ('with_qaofficer_completed', 'QA Officer Completed'),
        ('referral_complete','Referral Completed'),
    ]
    DEFAULT_TYPE = TYPE_CHOICES[0][0]

    #to = models.CharField(max_length=200, blank=True, verbose_name="To")
    to = models.TextField(blank=True, verbose_name="To")
    fromm = models.CharField(max_length=200, blank=True, verbose_name="From")
    #cc = models.CharField(max_length=200, blank=True, verbose_name="cc")
    cc = models.TextField(blank=True, verbose_name="cc")

    type = models.CharField(max_length=35, choices=TYPE_CHOICES, default=DEFAULT_TYPE)
    reference = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=200, blank=True, verbose_name="Subject / Description")
    text = models.TextField(blank=True)

    customer = models.ForeignKey(EmailUser, null=True, related_name='+')
    staff = models.ForeignKey(EmailUser, null=True, related_name='+')

    created = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        app_label = 'boranga'


@python_2_unicode_compatible
class Document(models.Model):
    name = models.CharField(max_length=255, blank=True,
                            verbose_name='name', help_text='')
    description = models.TextField(blank=True,
                                   verbose_name='description', help_text='')
    uploaded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'boranga'
        abstract = True

    @property
    def path(self):
        #return self.file.path
        #return self._file.path
        #comment above line to fix the error "The '_file' attribute has no file associated with it." when adding comms log entry.
        if self._file:
            return self._file.path
        else:
            return ''

    @property
    def filename(self):
        return os.path.basename(self.path)

    def __str__(self):
        return self.name or self.filename

class GlobalSettings(models.Model):
    keys = (
        ('credit_facility_link', 'Credit Facility Link'),
        ('deed_poll', 'Deed poll'),
        ('deed_poll_filming', 'Deed poll Filming'),
        ('deed_poll_event', 'Deed poll Event'),
        ('online_training_document', 'Online Training Document'),
        ('park_finder_link', 'Park Finder Link'),
        ('fees_and_charges', 'Fees and charges link'),
        ('event_fees_and_charges', 'Event Fees and charges link'),
        ('commercial_filming_handbook', 'Commercial Filming Handbook link'),
        ('park_stay_link', 'Park Stay Link'),
        ('event_traffic_code_of_practice', 'Event traffic code of practice'),
        ('trail_section_map', 'Trail section map'),
        ('dwer_application_form', 'DWER Application Form'),

    )
    key = models.CharField(max_length=255, choices=keys, blank=False, null=False,)
    value = models.CharField(max_length=255)

    class Meta:
        app_label = 'boranga'
        verbose_name_plural = "Global Settings"


@python_2_unicode_compatible
class SystemMaintenance(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def duration(self):
        """ Duration of system maintenance (in mins) """
        return int( (self.end_date - self.start_date).total_seconds()/60.) if self.end_date and self.start_date else ''
        #return (datetime.now(tz=tz) - self.start_date).total_seconds()/60.
    duration.short_description = 'Duration (mins)'

    class Meta:
        app_label = 'boranga'
        verbose_name_plural = "System maintenance"

    def __str__(self):
        return 'System Maintenance: {} ({}) - starting {}, ending {}'.format(self.name, self.description, self.start_date, self.end_date)

class UserSystemSettings(models.Model):
    one_row_per_park = models.BooleanField(default=False) #Setting for user if they want to see Payment (Park Entry Fees Dashboard) by one row per park or one row per booking
    user = models.ForeignKey(EmailUser, unique=True, related_name='system_settings')
    event_training_completed = models.BooleanField(default=False)
    event_training_date= models.DateField(blank=True, null=True)

    class Meta:
        app_label = 'boranga'
        verbose_name_plural = "User System Settings"


import reversion
reversion.register(Region, follow=['districts'])
reversion.register(District, follow=['parks'])
#reversion.register(AccessType)
reversion.register(AccessType, follow=['park_set', 'proposalparkaccess_set', 'vehicles'])
reversion.register(ActivityType)
reversion.register(ActivityCategory, follow=['activities'])
#reversion.register(Activity, follow=['park_set', 'zone_set', 'trail_set', 'requireddocument_set'])
reversion.register(Activity, follow=['park_set', 'zone_set', 'trail_set', 'requireddocument_set', 'proposalparkactivity_set','proposalparkzoneactivity_set', 'proposaltrailsectionactivity_set'])
#reversion.register(Park, follow=['zones', 'requireddocument_set', 'proposals', 'park_entries', 'bookings'])
reversion.register(Park, follow=['zones', 'requireddocument_set', 'proposals'])
reversion.register(Zone, follow=['proposal_zones'])
reversion.register(Trail, follow=['sections', 'proposals'])
reversion.register(Section, follow=['proposal_trails'])
reversion.register(RequiredDocument)
reversion.register(ApplicationType, follow=['tenure_app_types', 'helppage_set'])
reversion.register(ActivityMatrix)
reversion.register(Tenure)
reversion.register(Question)
reversion.register(UserAction)
reversion.register(CommunicationsLogEntry)
reversion.register(Document)
reversion.register(SystemMaintenance)

