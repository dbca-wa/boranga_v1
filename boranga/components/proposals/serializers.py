from django.conf import settings
from ledger.accounts.models import EmailUser,Address
from boranga.components.main.models import ApplicationType
from boranga.components.proposals.models import (
                                    ProposalType,
                                    Proposal,
                                    ProposalUserAction,
                                    ProposalLogEntry,
                                    Referral,
                                    ProposalRequirement,
                                    ProposalStandardRequirement,
                                    ProposalDeclinedDetails,
                                    AmendmentRequest,
                                    AmendmentReason,
                                    ProposalApplicantDetails,
                                    ChecklistQuestion,
                                    ProposalAssessmentAnswer,
                                    ProposalAssessment,
                                    RequirementDocument,
                                )
from boranga.components.organisations.models import (
                                Organisation
                            )
from boranga.components.main.serializers import CommunicationLogEntrySerializer
from boranga.components.organisations.serializers import OrganisationSerializer
from boranga.components.users.serializers import UserAddressSerializer, DocumentSerializer
from rest_framework import serializers
from django.db.models import Q
from reversion.models import Version

class ProposalTypeSerializer(serializers.ModelSerializer):
    activities = serializers.SerializerMethodField()
    class Meta:
        model = ProposalType
        fields = (
            'id',
            'schema',
            'activities'
        )


    def get_activities(self,obj):
        return obj.activities.names()

class EmailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailUser
        fields = ('id','email','first_name','last_name','title','organisation')

class EmailUserAppViewSerializer(serializers.ModelSerializer):
    residential_address = UserAddressSerializer()
    #identification = DocumentSerializer()

    class Meta:
        model = EmailUser
        fields = ('id',
                  'email',
                  'first_name',
                  'last_name',
                  'dob',
                  'title',
                  'organisation',
                  'residential_address',
                  #'identification',
                  'email',
                  'phone_number',
                  'mobile_number',)

class ProposalApplicantDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalApplicantDetails
        fields = ('id','first_name')

class ChecklistQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChecklistQuestion
        #fields = '__all__'
        fields=('id',
                'text',
                'answer_type',
                )
class ProposalAssessmentAnswerSerializer(serializers.ModelSerializer):
    question=ChecklistQuestionSerializer(read_only=True)
    class Meta:
        model = ProposalAssessmentAnswer
        fields = ('id',
                'question',
                'answer',
                'text_answer',
                )

class ProposalAssessmentSerializer(serializers.ModelSerializer):
    #checklist=ProposalAssessmentAnswerSerializer(many=True, read_only=True)
    checklist=serializers.SerializerMethodField()

    class Meta:
        model = ProposalAssessment
        fields = ('id',
                'completed',
                'submitter',
                'referral_assessment',
                'referral_group',
                'referral_group_name',
                'checklist'
                )

    def get_checklist(self,obj):
        qs= obj.checklist.order_by('question__order')
        return ProposalAssessmentAnswerSerializer(qs, many=True, read_only=True).data


class BaseProposalSerializer(serializers.ModelSerializer):
    #org_applicant = OrganisationSerializer()
    readonly = serializers.SerializerMethodField(read_only=True)
    documents_url = serializers.SerializerMethodField()
    proposal_type = serializers.SerializerMethodField()
    allowed_assessors = EmailUserSerializer(many=True)

    get_history = serializers.ReadOnlyField()

    class Meta:
        model = Proposal
        fields = (
                'id',
                'application_type',
                'proposal_type',
                'approval_level',
                'title',
                'region',
                'district',
                'data',
                'schema',
                'customer_status',
                'processing_status',
                'review_status',
                'applicant_type',
                'applicant',
                'org_applicant',
                'proxy_applicant',
                'submitter',
                'assigned_officer',
                'previous_application',
                'get_history',
                'lodgement_date',
                'modified_date',
                'documents',
                'requirements',
                'readonly',
                'can_user_edit',
                'can_user_view',
                'documents_url',
                'reference',
                'lodgement_number',
                'lodgement_sequence',
                'can_officer_process',
                'allowed_assessors',
                'proposal_type',
                'pending_amendment_request',
                'is_amendment_proposal',

                # tab field models
                'applicant_details',

                )
        read_only_fields=('documents',)

    def get_documents_url(self,obj):
        return '/media/{}/proposals/{}/documents/'.format(settings.MEDIA_APP_DIR, obj.id)

    def get_readonly(self,obj):
        return False

    def get_processing_status(self,obj):
        return obj.get_processing_status_display()

    def get_review_status(self,obj):
        return obj.get_review_status_display()

    def get_customer_status(self,obj):
        return obj.get_customer_status_display()

    def get_proposal_type(self,obj):
        return obj.get_proposal_type_display()


class ListProposalSerializer(BaseProposalSerializer):
    submitter = EmailUserSerializer()
    applicant = serializers.CharField(read_only=True)
    processing_status = serializers.SerializerMethodField(read_only=True)
    review_status = serializers.SerializerMethodField(read_only=True)
    customer_status = serializers.SerializerMethodField(read_only=True)
    assigned_officer = serializers.SerializerMethodField(read_only=True)

    application_type = serializers.CharField(source='application_type.name', read_only=True)
    region = serializers.SerializerMethodField(read_only=True)
    district = serializers.SerializerMethodField(read_only=True)

    assessor_process = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Proposal
        fields = (
                'id',
                'application_type',
                'proposal_type',
                'activity',
                'approval_level',
                'title',
                'region',
                'district',
                'tenure',
                'customer_status',
                'processing_status',
                'review_status',
                'applicant',
                'proxy_applicant',
                'submitter',
                'assigned_officer',
                'previous_application',
                'get_history',
                'lodgement_date',
                'modified_date',
                'readonly',
                'can_user_edit',
                'can_user_view',
                'reference',
                'lodgement_number',
                'lodgement_sequence',
                'can_officer_process',
                'assessor_process',
                'allowed_assessors',
                'proposal_type',
                )
        # the serverSide functionality of datatables is such that only columns that have field 'data' defined are requested from the serializer. We
        # also require the following additional fields for some of the mRender functions
        datatables_always_serialize = (
                'id',
                'proposal_type',
                'activity',
                'title',
                'region',
                'customer_status',
                'processing_status',
                'applicant',
                'submitter',
                'assigned_officer',
                'lodgement_date',
                'can_user_edit',
                'can_user_view',
                'reference',
                'lodgement_number',
                'can_officer_process',
                'assessor_process',
                'allowed_assessors',
                )

    def get_assigned_officer(self,obj):
        if obj.processing_status==Proposal.PROCESSING_STATUS_WITH_APPROVER and obj.assigned_approver:
            return obj.assigned_approver.get_full_name()
        if obj.assigned_officer:
            return obj.assigned_officer.get_full_name()
        return None

    def get_region(self,obj):
        if obj.region:
            return obj.region.name
        return None

    def get_district(self,obj):
        if obj.district:
            return obj.district.name
        return None

    def get_assessor_process(self,obj):
        # Check if currently logged in user has access to process the proposal
        request = self.context['request']
        user = request.user
        if obj.can_officer_process:
            '''if (obj.assigned_officer and obj.assigned_officer == user) or (user in obj.allowed_assessors):
                return True'''
            if obj.assigned_officer:
                if obj.assigned_officer == user:
                    return True
            elif user in obj.allowed_assessors:
                return True
        return False


class ProposalSerializer(BaseProposalSerializer):
    submitter = serializers.CharField(source='submitter.get_full_name')
    processing_status = serializers.SerializerMethodField(read_only=True)
    review_status = serializers.SerializerMethodField(read_only=True)
    customer_status = serializers.SerializerMethodField(read_only=True)

    application_type = serializers.CharField(source='application_type.name', read_only=True)
    region = serializers.CharField(source='region.name', read_only=True)
    district = serializers.CharField(source='district.name', read_only=True)

    def get_readonly(self,obj):
        return obj.can_user_view


class SaveProposalSerializer(BaseProposalSerializer):
    assessor_data = serializers.JSONField(required=False)

    class Meta:
        model = Proposal
        fields = (
                'id',
                'application_type',
                'activity',
                'approval_level',
                'title',
                'region',
                'district',
                'tenure',
                'data',
                'assessor_data',
                'comment_data',
                'schema',
                'customer_status',
                'processing_status',
                'review_status',
                #'hard_copy',
                'applicant_type',
                'applicant',
                'org_applicant',
                'proxy_applicant',
                'submitter',
                'assigned_officer',
                'previous_application',
                'lodgement_date',
                'documents',
                'requirements',
                'readonly',
                'can_user_edit',
                'can_user_view',
                'reference',
                'lodgement_number',
                'lodgement_sequence',
                'can_officer_process',
                'applicant_details',
                )
        read_only_fields=('documents','requirements',)



class ApplicantSerializer(serializers.ModelSerializer):
    from boranga.components.organisations.serializers import OrganisationAddressSerializer
    address = OrganisationAddressSerializer(read_only=True)
    class Meta:
        model = Organisation
        fields = (
                    'id',
                    'name',
                    'abn',
                    'address',
                    'email',
                    'phone_number',
                )


class ProposalReferralSerializer(serializers.ModelSerializer):
    referral = serializers.CharField(source='referral_group.name')
    processing_status = serializers.CharField(source='get_processing_status_display')
    class Meta:
        model = Referral
        fields = '__all__'


class ProposalDeclinedDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalDeclinedDetails
        fields = '__all__'


class InternalProposalSerializer(BaseProposalSerializer):
    applicant = serializers.CharField(read_only=True)
    org_applicant = OrganisationSerializer()
    processing_status = serializers.SerializerMethodField(read_only=True)
    review_status = serializers.SerializerMethodField(read_only=True)
    customer_status = serializers.SerializerMethodField(read_only=True)
    submitter = EmailUserAppViewSerializer()
    proposaldeclineddetails = ProposalDeclinedDetailsSerializer()
    #
    assessor_mode = serializers.SerializerMethodField()
    can_edit_activities = serializers.SerializerMethodField()
    can_edit_period = serializers.SerializerMethodField()
    current_assessor = serializers.SerializerMethodField()
    assessor_data = serializers.SerializerMethodField()
    latest_referrals = ProposalReferralSerializer(many=True)
    allowed_assessors = EmailUserSerializer(many=True)
    approval_level_document = serializers.SerializerMethodField()
    application_type = serializers.CharField(source='application_type.name', read_only=True)
    region = serializers.CharField(source='region.name', read_only=True)
    district = serializers.CharField(source='district.name', read_only=True)
    assessor_assessment=ProposalAssessmentSerializer(read_only=True)
    referral_assessments=ProposalAssessmentSerializer(read_only=True, many=True)
    requirements_completed=serializers.SerializerMethodField()

    class Meta:
        model = Proposal
        fields = (
                'id',
                'application_type',
                'activity',
                'approval_level',
                'approval_level_document',
                'region',
                'district',
                'tenure',
                'title',
                'data',
                'schema',
                'customer_status',
                'processing_status',
                'review_status',
                #'hard_copy',
                'applicant',
                'org_applicant',
                'proxy_applicant',
                'submitter',
                'applicant_type',
                'assigned_officer',
                'assigned_approver',
                'previous_application',
                'get_history',
                'lodgement_date',
                'modified_date',
                'documents',
                'requirements',
                'readonly',
                'can_user_edit',
                'can_user_view',
                'documents_url',
                'assessor_mode',
                'current_assessor',
                'assessor_data',
                'comment_data',
                'latest_referrals',
                'allowed_assessors',
                'proposed_issuance_approval',
                'proposed_decline_status',
                'proposaldeclineddetails',
                'permit',
                'reference',
                'lodgement_number',
                'lodgement_sequence',
                'can_officer_process',
                'proposal_type',
                # tab field models
                'applicant_details',
                'assessor_assessment',
                'referral_assessments',
                'requirements_completed'
                )
        read_only_fields=('documents','requirements')

    def get_approval_level_document(self,obj):
        if obj.approval_level_document is not None:
            return [obj.approval_level_document.name,obj.approval_level_document._file.url]
        else:
            return obj.approval_level_document

    def get_assessor_mode(self,obj):
        # TODO check if the proposal has been accepted or declined
        request = self.context['request']
        user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
        return {
            'assessor_mode': True,
            'has_assessor_mode': obj.has_assessor_mode(user),
            'assessor_can_assess': obj.can_assess(user),
            'assessor_level': 'assessor',
            'assessor_box_view': obj.assessor_comments_view(user)
        }

    def get_readonly(self,obj):
        return True

    def get_requirements_completed(self,obj):
        return True

    def get_current_assessor(self,obj):
        return {
            'id': self.context['request'].user.id,
            'name': self.context['request'].user.get_full_name(),
            'email': self.context['request'].user.email
        }

    def get_assessor_data(self,obj):
        return obj.assessor_data


class ProposalUserActionSerializer(serializers.ModelSerializer):
    who = serializers.CharField(source='who.get_full_name')
    class Meta:
        model = ProposalUserAction
        fields = '__all__'

class ProposalLogEntrySerializer(CommunicationLogEntrySerializer):
    documents = serializers.SerializerMethodField()
    class Meta:
        model = ProposalLogEntry
        fields = '__all__'
        read_only_fields = (
            'customer',
        )

    def get_documents(self,obj):
        return [[d.name,d._file.url] for d in obj.documents.all()]

class SendReferralSerializer(serializers.Serializer):
    email_group = serializers.CharField()
    text = serializers.CharField(allow_blank=True)

class DTReferralSerializer(serializers.ModelSerializer):
    processing_status = serializers.CharField(source='proposal.get_processing_status_display')
    application_type = serializers.CharField(source='proposal.application_type.name')
    referral_status = serializers.CharField(source='get_processing_status_display')
    proposal_lodgement_date = serializers.CharField(source='proposal.lodgement_date')
    proposal_lodgement_number = serializers.CharField(source='proposal.lodgement_number')
    submitter = serializers.SerializerMethodField()
    region = serializers.CharField(source='region.name', read_only=True)
    referral = serializers.CharField(source='referral_group.name')
    document = serializers.SerializerMethodField()
    can_user_process=serializers.SerializerMethodField()
    assigned_officer = serializers.CharField(source='assigned_officer.get_full_name', allow_null=True)
    class Meta:
        model = Referral
        fields = (
            'id',
            'region',
            'activity',
            'title',
            'applicant',
            'submitter',
            'processing_status',
            'application_type',
            'referral_status',
            'lodged_on',
            'proposal',
            'can_be_processed',
            'referral',
            'proposal_lodgement_date',
            'proposal_lodgement_number',
            'referral_text',
            'document',
            'assigned_officer',
            'can_user_process',
        )

    def get_submitter(self,obj):
        return EmailUserSerializer(obj.proposal.submitter).data

    def get_document(self,obj):
        return [obj.document.name, obj.document._file.url] if obj.document else None

    def get_can_user_process(self,obj):
        request = self.context['request']
        user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
        if obj.can_process(user) and obj.can_be_completed:
            if obj.assigned_officer:
                if obj.assigned_officer == user:
                    return True
            else:
                return True
        return False



class RequirementDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementDocument
        fields = ('id', 'name', '_file')
        #fields = '__all__'

class ProposalRequirementSerializer(serializers.ModelSerializer):
    due_date = serializers.DateField(input_formats=['%d/%m/%Y'],required=False,allow_null=True)
    can_referral_edit=serializers.SerializerMethodField()
    requirement_documents = RequirementDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = ProposalRequirement
        fields = (
            'id',
            'due_date',
            'free_requirement',
            'standard_requirement',
            'standard','order',
            'proposal',
            'recurrence',
            'recurrence_schedule',
            'recurrence_pattern',
            'requirement',
            'is_deleted',
            'copied_from',
            'referral_group',
            'can_referral_edit',
            'district',
            'requirement_documents',
            'require_due_date',
            'copied_for_renewal',
            'notification_only',
        )
        read_only_fields = ('order','requirement', 'copied_from')

    def get_can_referral_edit(self,obj):
        request = self.context['request']
        user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
        return obj.can_referral_edit(user)


class ProposalStandardRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalStandardRequirement
        fields = ('id','code','text')

class ProposedApprovalSerializer(serializers.Serializer):
    expiry_date = serializers.DateField(input_formats=['%d/%m/%Y'])
    start_date = serializers.DateField(input_formats=['%d/%m/%Y'])
    details = serializers.CharField()
    cc_email = serializers.CharField(required=False,allow_null=True)

class PropedDeclineSerializer(serializers.Serializer):
    reason = serializers.CharField()
    cc_email = serializers.CharField(required=False, allow_null=True)


class AmendmentRequestSerializer(serializers.ModelSerializer):
    #reason = serializers.SerializerMethodField()

    class Meta:
        model = AmendmentRequest
        fields = '__all__'


class AmendmentRequestDisplaySerializer(serializers.ModelSerializer):
    reason = serializers.SerializerMethodField()

    class Meta:
        model = AmendmentRequest
        fields = '__all__'

    def get_reason (self,obj):
        return obj.reason.reason if obj.reason else None


class SearchKeywordSerializer(serializers.Serializer):
    number = serializers.CharField()
    id = serializers.IntegerField()
    type = serializers.CharField()
    applicant = serializers.CharField()
    #text = serializers.CharField(required=False,allow_null=True)
    text = serializers.JSONField(required=False)

class SearchReferenceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()


class ReferralProposalSerializer(InternalProposalSerializer):
    def get_assessor_mode(self,obj):
        # TODO check if the proposal has been accepted or declined
        request = self.context['request']
        user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
        try:
            referral = Referral.objects.get(proposal=obj,referral=user)
        except:
            referral = None
        return {
            'assessor_mode': True,
            'assessor_can_assess': referral.can_assess_referral(user) if referral else None,
            'assessor_level': 'referral',
            'assessor_box_view': obj.assessor_comments_view(user)
        }


class ReferralSerializer(serializers.ModelSerializer):
    processing_status = serializers.CharField(source='get_processing_status_display')
    latest_referrals = ProposalReferralSerializer(many=True)
    can_be_completed = serializers.BooleanField()
    can_process=serializers.SerializerMethodField()
    referral_assessment=ProposalAssessmentSerializer(read_only=True)
    application_type=serializers.CharField(read_only=True)
    allowed_assessors = EmailUserSerializer(many=True)
    current_assessor = serializers.SerializerMethodField()

    class Meta:
        model = Referral
        fields = '__all__'

    def get_current_assessor(self,obj):
        return {
            'id': self.context['request'].user.id,
            'name': self.context['request'].user.get_full_name(),
            'email': self.context['request'].user.email
        }


    def __init__(self,*args,**kwargs):
        super(ReferralSerializer, self).__init__(*args, **kwargs)
        try:
            if kwargs.get('context')['view'].get_object().proposal.application_type.name == ApplicationType.TCLASS:
                self.fields['proposal'] = ReferralProposalSerializer(context={'request':self.context['request']})
            elif kwargs.get('context')['view'].get_object().proposal.application_type.name == ApplicationType.FILMING:
                self.fields['proposal'] = FilmingReferralProposalSerializer(context={'request':self.context['request']})
            elif kwargs.get('context')['view'].get_object().proposal.application_type.name == ApplicationType.EVENT:
                self.fields['proposal'] = EventReferralProposalSerializer(context={'request':self.context['request']})
        except:
            raise

    def get_can_process(self,obj):
        request = self.context['request']
        user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
        return obj.can_process(user)
