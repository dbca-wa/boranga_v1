<template lang="html">
    <div>
        <!-- <div class="col-md-3" >
            <div class="panel panel-default fixed">
              <div class="panel-heading">
                <h5>Sections</h5>
              </div>
              <div class="panel-body" style="padding:0">
                  <ul class="list-group" id="scrollspy-section" style="margin-bottom:0">

                  </ul>
              </div>
            </div>
        </div> -->

        <div class="col-md-12">
            <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
              <li class="nav-item">
                <a class="nav-link active" id="pills-applicant-tab" data-toggle="pill" href="#pills-applicant" role="tab" aria-controls="pills-applicant" aria-selected="true">
                  1. Applicant
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" id="pills-activity-tab" data-toggle="pill" href="#pills-activity" role="tab" aria-controls="pills-activity" aria-selected="false">
                  2. Activity
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" id="pills-access-tab" data-toggle="pill" href="#pills-access" role="tab" aria-controls="pills-access" aria-selected="false">
                  3. Access
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" id="pills-equipment-tab" data-toggle="pill" href="#pills-equipment" role="tab" aria-controls="pills-equipment" aria-selected="false">
                  4. Equipment
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" id="pills-other-details-tab" data-toggle="pill" href="#pills-other-details" role="tab" aria-controls="pills-other-details" aria-selected="false">
                  5. Other Details
                </a>
              </li>
              <li v-if="is_external" class="nav-item" id="li-confirm">
                <a class="nav-link disabled" id="pills-confirm-tab" data-toggle="pill" href="" role="tab" aria-controls="pills-confirm" aria-selected="false">
                  6. Confirmation
                </a>
              </li>

            </ul>
            <div class="tab-content" id="pills-tabContent">

              <div class="tab-pane fade" id="pills-applicant" role="tabpanel" aria-labelledby="pills-applicant-tab">
                  <div v-if="is_external">
                    <Profile :isApplication="true" v-if="applicantType == 'SUB'" ref="profile"></Profile>
              
                    <Organisation :org_id="proposal.org_applicant" :isApplication="true" v-if="applicantType == 'ORG'" ref="organisation"></Organisation> 
                  </div>
                  <div v-else>
                    <Applicant :proposal="proposal" id="proposalStartApplicant"></Applicant>
                    <div v-if="is_internal || is_referral">
                      <ApprovalType :proposal="proposal" :hasAssessorMode="hasAssessorMode"></ApprovalType>
                    </div>
                    <div v-if="is_internal">
                      <Assessment :proposal="proposal" :assessment="proposal.assessor_assessment" :hasAssessorMode="hasAssessorMode" :is_internal="is_internal" :is_referral="is_referral"></Assessment>
                      <div v-for="assess in proposal.referral_assessments">
                        <Assessment :proposal="proposal" :assessment="assess"></Assessment>
                      </div>

                    </div>
                  </div>
              </div>

              <div class="tab-pane fade" id="pills-activity" role="tabpanel" aria-labelledby="pills-activity-tab">
                <Activity :proposal="proposal" id="proposalStartActivity" :hasDistrictAssessorMode="hasDistrictAssessorMode" :district_proposal= "district_proposal" :canEditActivities="canEditActivities" :canEditPeriod="canEditPeriod" :is_external= "is_external"></Activity>
              </div>
              <div class="tab-pane fade" id="pills-access" role="tabpanel" aria-labelledby="pills-access-tab">
                <Access :proposal="proposal" id="proposalStartAccess" :hasDistrictAssessorMode="hasDistrictAssessorMode" :district_proposal= "district_proposal" :canEditActivities="canEditActivities" :canEditPeriod="canEditPeriod" :is_external= "is_external" ref="filming_access"></Access>
              </div>
              <div class="tab-pane fade" id="pills-equipment" role="tabpanel" aria-labelledby="pills-equipment-tab">
                <Equipment :proposal="proposal" id="proposalStartEquipment" ref="filming_equipment"></Equipment>
              </div>
              <div class="tab-pane fade" id="pills-other-details" role="tabpanel" aria-labelledby="pills-other-details-tab">
                <OtherDetails :proposal="proposal" id="proposalStartOtherDetails" ref="filming_other_details"></OtherDetails>
              </div>
              <div class="tab-pane fade" id="pills-confirm" role="tabpanel" aria-labelledby="pills-confirm-tab">
                <Confirmation :proposal="proposal" id="proposalStartConfirmation"></Confirmation>
              </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Profile from '@/components/user/profile.vue'
    import Organisation from '@/components/external/organisations/manage.vue'
    import Applicant from '@/components/common/tclass/applicant.vue'
    import Assessment from '@/components/common/tclass/assessment.vue'

    //import Applicant from '@/components/common/filming/applicant.vue'
    import ApprovalType from '@/components/common/filming/approval_type.vue'
    import Activity from '@/components/common/filming/activity.vue'
    import Access from '@/components/common/filming/access.vue'
    import Equipment from '@/components/common/filming/equipment.vue'
    import OtherDetails from '@/components/common/filming/other_details.vue'
    import OnlineTraining from '@/components/common/filming/online_training.vue'
    import Payment from '@/components/common/filming/payment.vue'
    import Confirmation from '@/components/common/filming/confirmation.vue'
    export default {
        props:{
            proposal:{
                type: Object,
                required:true
            },
            canEditActivities:{
              type: Boolean,
              default: true
            },
            canEditPeriod:{
              type: Boolean,
              default: false
            },
            is_external:{
              type: Boolean,
              default: false
            },
            is_internal:{
              type: Boolean,
              default: false
            },
            is_referral:{
              type: Boolean,
              default: false
            },
            hasReferralMode:{
                type:Boolean,
                default: false
            },
            hasAssessorMode:{
                type:Boolean,
                default: false
            },
            referral:{
                type: Object,
                required:false
            },
            proposal_parks:{
                type:Object,
                default:null
            },
            hasDistrictAssessorMode:{
                type:Boolean,
                default: false
            },
            district_proposal:{
                type:Object,
                default:null
            },
        },
        data:function () {
            return{
                values:null
            }
        },
        components: {
            Applicant,
            Activity,
            Access,
            Equipment,
            OtherDetails,
            Confirmation,
            Profile,
            Organisation,
            Assessment,
            ApprovalType
        },
        computed:{
          applicantType: function(){
            return this.proposal.applicant_type;
          },
        },
        methods:{
          set_tabs:function(){
                let vm = this;

                /* Confirmation tab - Always Disabled */
                $('#pills-confirm-tab').attr('style', 'background-color:#E5E8E8 !important; color: #99A3A4;');
                $('#li-confirm').attr('class', 'nav-item disabled');
            },
            eventListener: function(){
              let vm=this;
              $('a[href="#pills-access"]').on('shown.bs.tab', function (e) {
                vm.$refs.filming_access.$refs.parks_table.$refs.park_datatable.vmDataTable.columns.adjust().responsive.recalc();
              });
              $('a[href="#pills-equipment"]').on('shown.bs.tab', function (e) {
                vm.$refs.filming_equipment.$refs.vessel_table.$refs.vessel_datatable.vmDataTable.columns.adjust().responsive.recalc();
              });
            },
        },
        mounted: function() {
            let vm = this;
            $('#pills-tab a[href="#pills-applicant"]').tab('show');
            vm.set_tabs();
            vm.eventListener();
            vm.form = document.forms.new_proposal;
            //window.addEventListener('beforeunload', vm.leaving);
            //indow.addEventListener('onblur', vm.leaving);
        }
 
    }
</script>

<style lang="css" scoped>
    .section{
        text-transform: capitalize;
    }
    .list-group{
        margin-bottom: 0;
    }
    .fixed-top{
        position: fixed;
        top:56px;
    }

    .nav-item {
        background-color: rgb(200,200,200,0.8) !important;
        margin-bottom: 2px;
    }

    .nav-item>li>a {
        background-color: yellow !important;
        color: #fff;
    }

    .nav-item>li.active>a, .nav-item>li.active>a:hover, .nav-item>li.active>a:focus {
      color: white;
      background-color: blue;
      border: 1px solid #888888;
    }

	.admin > div {
	  display: inline-block;
	  vertical-align: top;
	  margin-right: 1em;
	}
</style>

