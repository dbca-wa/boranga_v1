from django.contrib import admin
from ledger.accounts.models import EmailUser
from boranga.components.proposals import models
from boranga.components.proposals import forms
from boranga.components.main.models import (
    SystemMaintenance,
    ApplicationType,
    Question,
    GlobalSettings,
)
#from boranga.components.main.models import Activity, SubActivityLevel1, SubActivityLevel2, SubCategory
from reversion.admin import VersionAdmin
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from boranga.utils import create_helppage_object
# Register your models here.

# Commented since COLS does not use schema - so will not require direct editing by user in Admin (although a ProposalType is still required for ApplicationType)
#@admin.register(models.ProposalType)
class ProposalTypeAdmin(admin.ModelAdmin):
    list_display = ['name','description', 'version']
    ordering = ('name', '-version')
    list_filter = ('name',)
    #exclude=("site",)

class ProposalDocumentInline(admin.TabularInline):
    model = models.ProposalDocument
    extra = 0

@admin.register(models.AmendmentReason)
class AmendmentReasonAdmin(admin.ModelAdmin):
    list_display = ['reason']

@admin.register(models.Proposal)
class ProposalAdmin(VersionAdmin):
    inlines =[ProposalDocumentInline,]

@admin.register(models.ProposalAssessorGroup)
class ProposalAssessorGroupAdmin(admin.ModelAdmin):
    list_display = ['name','default']
    filter_horizontal = ('members',)
    form = forms.ProposalAssessorGroupAdminForm
    readonly_fields = ['default']
    #readonly_fields = ['regions', 'activities']

    def get_actions(self, request):
        actions =  super(ProposalAssessorGroupAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        if self.model.objects.count() == 1:
            return False
        return super(ProposalAssessorGroupAdmin, self).has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return super(ProposalAssessorGroupAdmin, self).has_add_permission(request)


@admin.register(models.ProposalApproverGroup)
class ProposalApproverGroupAdmin(admin.ModelAdmin):
    list_display = ['name','default']
    filter_horizontal = ('members',)
    form = forms.ProposalApproverGroupAdminForm
    readonly_fields = ['default']
    #readonly_fields = ['default', 'regions', 'activities']

    def get_actions(self, request):
        actions =  super(ProposalApproverGroupAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        if self.model.objects.count() == 1:
            return False
        return super(ProposalApproverGroupAdmin, self).has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return super(ProposalApproverGroupAdmin, self).has_add_permission(request)

@admin.register(models.ProposalStandardRequirement)
class ProposalStandardRequirementAdmin(admin.ModelAdmin):
    list_display = ['code','text','obsolete', 'application_type', 'participant_number_required', 'default']

#@admin.register(models.HelpPage)
class HelpPageAdmin(admin.ModelAdmin):
    list_display = ['application_type','help_type', 'description', 'version']
    form = forms.CommercialOperatorHelpPageAdminForm
    change_list_template = "boranga/help_page_changelist.html"
    ordering = ('application_type', 'help_type', '-version')
    list_filter = ('application_type', 'help_type')


    def get_urls(self):
        urls = super(HelpPageAdmin, self).get_urls()
        my_urls = [
            url('create_boranga_help/', self.admin_site.admin_view(self.create_boranga_help)),
            url('create_boranga_help_assessor/', self.admin_site.admin_view(self.create_boranga_help_assessor)),
        ]
        return my_urls + urls

    def create_boranga_help(self, request):
        create_helppage_object(application_type='T Class', help_type=models.HelpPage.HELP_TEXT_EXTERNAL)
        return HttpResponseRedirect("../")

    def create_boranga_help_assessor(self, request):
        create_helppage_object(application_type='T Class', help_type=models.HelpPage.HELP_TEXT_INTERNAL)
        return HttpResponseRedirect("../")

@admin.register(models.ChecklistQuestion)
class ChecklistQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'application_type','list_type', 'obsolete','answer_type', 'order']
    ordering = ('order',)

@admin.register(SystemMaintenance)
class SystemMaintenanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'start_date', 'end_date', 'duration']
    ordering = ('start_date',)
    readonly_fields = ('duration',)
    form = forms.SystemMaintenanceAdminForm

@admin.register(ApplicationType)
class ApplicationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'visible']
    ordering = ('order',)
    readonly_fields = ['name']

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']
    ordering = ('key',)

@admin.register(models.ReferralRecipientGroup)
class ReferralRecipientGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
    list_display = ['name']
    exclude = ('site',)
    actions = None

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            kwargs["queryset"] = EmailUser.objects.filter(is_staff=True)
        return super(ReferralRecipientGroupAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'answer_one', 'answer_two', 'answer_three', 'answer_four', 'application_type',]
    ordering = ('question_text',)
