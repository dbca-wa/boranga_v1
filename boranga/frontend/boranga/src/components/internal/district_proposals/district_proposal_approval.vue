<template id="district_proposal_approval">
    <div>
        <template v-if="isFinalised">
            <div class="col-md-12 alert alert-success" v-if="district_proposal.processing_status == 'Approved'">
                <p>The Lawful Authority has been issued and has been emailed to {{district_proposal.proposal.applicant}}</p>
                <p>Expiry date: {{district_proposal.proposed_issuance_approval.expiry_date}}
                <p>Lawful Authority: <a target="_blank" :href="district_proposal.proposal.permit">lawful_authority.pdf</a></p>
            </div>
            <div v-else class="col-md-12 alert alert-warning">
                <p>The application was declined. The decision was emailed to {{district_proposal.proposal.applicant}}</p>
            </div>    
        </template>
        
        <div class="col-md-12">
            <div class="row">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h3 v-if="!isFinalised" class="panel-title">Proposed Decision
                            <a class="panelClicker" :href="'#'+proposedDecision" data-toggle="collapse"  data-parent="#userInfo" expanded="false" :aria-controls="proposedDecision">
                                <span class="glyphicon glyphicon-chevron-down pull-right "></span>
                            </a>
                        </h3>
                        <h3 v-else class="panel-title">Decision
                            <a class="panelClicker" :href="'#'+proposedDecision" data-toggle="collapse"  data-parent="#userInfo" expanded="false" :aria-controls="proposedDecision">
                                <span class="glyphicon glyphicon-chevron-down pull-right "></span>
                            </a>
                        </h3>
                    </div>
                    <div class="panel-body panel-collapse collapse in" :id="proposedDecision">
                        <div class="row">
                            <div class="col-sm-12">
                                <template v-if="!district_proposal.proposed_decline_status">
                                    <template v-if="isFinalised">
                                        <p><strong>Decision: Issue</strong></p>
                                        <p><strong>Start date: {{district_proposal.proposed_issuance_approval.start_date}}</strong></p>
                                        <p><strong>Expiry date: {{district_proposal.proposed_issuance_approval.expiry_date}}</strong></p>
                                        <p><strong>CC emails: {{district_proposal.proposed_issuance_approval.cc_email}}</strong></p>
                                    </template>
                                    <template v-else>
                                        <p><strong>Proposed decision: Issue</strong></p>
                                        <p><strong>Proposed start date: {{district_proposal.proposed_issuance_approval.start_date}}</strong></p>
                                        <p><strong>Proposed expiry date: {{district_proposal.proposed_issuance_approval.expiry_date}}</strong></p>
                                        <p><strong>Proposed cc emails: {{district_proposal.proposed_issuance_approval.cc_email}}</strong></p>
                                    </template>
                                </template>
                                <template v-else>
                                    <strong v-if="!isFinalised">Proposed decision: Decline</strong>
                                    <strong v-else>Decision: Decline</strong>
                                </template>
                            </div>
                        </div> 
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import {
    api_endpoints,
    helpers
}
from '@/utils/hooks'
import datatable from '@vue-utils/datatable.vue'
export default {
    name: 'InternalProposalApproval',
    props: {
        district_proposal: Object
    },
    data: function() {
        let vm = this;
        return {
            proposedDecision: "district_proposal-decision-"+vm._uid,
            proposedLevel: "district_proposal-level-"+vm._uid,
            uploadedFile: null,
        }
    },
    watch:{
    },
    components:{
    },
    computed:{
        // hasAssessorMode(){
        //     return this.district_proposal.assessor_mode.has_assessor_mode;
        // },
        isFinalised: function(){
            return this.district_proposal.processing_status == 'Approved' || this.district_proposal.processing_status == 'Declined';
        },
        // isApprovalLevel:function(){
        //     return this.district_proposal.approval_level != null ? true : false;
        // },
    },
    methods:{
        readFile: function() {
            let vm = this;
            let _file = null;
            var input = $(vm.$refs.uploadedFile)[0];
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.readAsDataURL(input.files[0]); 
                reader.onload = function(e) {
                    _file = e.target.result;
                };
                _file = input.files[0];
            }
            vm.uploadedFile = _file;
            vm.save()
        },
        removeFile: function(){
            let vm = this;
            vm.uploadedFile = null;
            vm.save()
        },
        save: function(){
            let vm = this;
                let data = new FormData(vm.form);
                data.append('approval_level_document', vm.uploadedFile)
                if (vm.district_proposal.approval_level_document) {
                    data.append('approval_level_document_name', vm.district_proposal.approval_level_document[0])
                }
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.district_proposals,vm.district_proposal.id+'/approval_level_document'),data,{
                emulateJSON:true
            }).then(res=>{
                vm.district_proposal = res.body;
                vm.$emit('refreshFromResponse',res);

                },err=>{
                swal(
                    'Submit Error',
                    helpers.apiVueResourceError(err),
                    'error'
                )
            });

            
        },
        uploadedFileName: function() {
            return this.uploadedFile != null ? this.uploadedFile.name: '';
        },
        addRequirement(){
            this.$refs.requirement_detail.isModalOpen = true;
        },
        removeRequirement(_id){
            let vm = this;
            swal({
                title: "Remove Requirement",
                text: "Are you sure you want to remove this requirement?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Remove Requirement',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(helpers.add_endpoint_json(api_endpoints.district_proposal_requirements,_id))
                .then((response) => {
                    vm.$refs.requirements_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {
            });
        },
    },
    mounted: function(){
        let vm = this;
    }
}
</script>
<style scoped>
</style>
