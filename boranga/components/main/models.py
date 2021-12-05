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


@python_2_unicode_compatible
class RequiredDocument(models.Model):
    question = models.TextField(blank=False)

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
    TCLASS = 'Commercial operations'
    name = models.CharField(max_length=64, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    visible = models.BooleanField(default=True)

    application_fee = models.DecimalField('Application Fee', max_digits=6, decimal_places=2, null=True)
    oracle_code_application = models.CharField(max_length=50)
    oracle_code_licence = models.CharField(max_length=50)
    is_gst_exempt = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        app_label = 'boranga'

    def __str__(self):
        return self.name


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
    user = models.ForeignKey(EmailUser, unique=True, related_name='system_settings')

    class Meta:
        app_label = 'boranga'
        verbose_name_plural = "User System Settings"


import reversion
#reversion.register(Region, follow=['districts'])

