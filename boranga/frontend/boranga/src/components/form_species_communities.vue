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
                <a class="nav-link active" id="pills-species-tab" data-toggle="pill" href="#pills-species" role="tab" aria-controls="pills-species" aria-selected="true">
                  Species
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" id="pills-documents-tab" data-toggle="pill" href="#pills-documents" role="tab" aria-controls="pills-documents" aria-selected="false">
                  Documents
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" id="pills-conservation-tab" data-toggle="pill" href="#pills-conservation" role="tab" aria-controls="pills-conservation" aria-selected="false">
                  Conservation
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" id="pills-management-plans-tab" data-toggle="pill" href="#pills-management-plans" role="tab" aria-controls="pills-management-plans" aria-selected="false">
                  Management Plans
                </a>
              </li>
              <li v-if="is_internal" class="nav-item" id="li-relate-items">
                <a class="nav-link" id="pills-related-items-tab" data-toggle="pill" href="#pills-related-items" role="tab" aria-controls="pills-related-items" aria-selected="false">
                  Related Items
                </a>
              </li>
            </ul>
            <div class="tab-content" id="pills-tabContent">
              <div class="tab-pane fade" id="pills-species" role="tabpanel" aria-labelledby="pills-species-tab">
                <Species :proposal="proposal" id="proposalSpecies" :canEditActivities="canEditActivities" ref="species" :is_external="is_external"></Species>
              </div>
              <div class="tab-pane fade" id="pills-documents" role="tabpanel" aria-labelledby="pills-documents-tab">
                <Documents :proposal="proposal" id="proposalDocuments" :canEditActivities="canEditActivities" ref="documents" :is_external="is_external"></Documents>
              </div>
              <div class="tab-pane fade" id="pills-conservation" role="tabpanel" aria-labelledby="pills-conservation-tab">
                <Conservation :proposal="proposal" id="proposalConservation" :canEditActivities="canEditActivities" ref="conservation" :is_external="is_external"></Conservation>
              </div>
              <div class="tab-pane fade" id="pills-management-plans" role="tabpanel" aria-labelledby="pills-management-plans-tab">
                <ManagementPlans :proposal="proposal" id="proposalManagementPlans" ref="management_plans"></ManagementPlans>
              </div>
              <div class="tab-pane fade" id="pills-related-items" role="tabpanel" aria-labelledby="pills-related-items-tab">
                <RelatedItems :proposal="proposal" id="proposalRelatedItems"></RelatedItems>
              </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Species from '@/components/common/species_communities/species.vue'
    import Documents from '@/components/common/species_communities/documents.vue'
    import Conservation from '@/components/common/species_communities/conservation.vue'
    import ManagementPlans from '@/components/common/species_communities/management_plans.vue'
    import RelatedItems from '@/components/common/species_communities/related_items.vue'

//    import Profile from '@/components/user/profile.vue'
//    import Organisation from '@/components/external/organisations/manage.vue'
//    import Applicant from '@/components/common/tclass/applicant.vue'
//    import Assessment from '@/components/common/tclass/assessment.vue'
//    import ActivitiesLand from '@/components/common/tclass/activities_land.vue'
//    import ActivitiesMarine from '@/components/common/tclass/activities_marine.vue'
//    import OtherDetails from '@/components/common/tclass/other_details.vue'
//    import OnlineTraining from '@/components/common/tclass/online_training.vue'
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
        },
        data:function () {
            return{
                values:null
            }
        },
        components: {
            Species,
            Documents,
            Conservation,
            ManagementPlans,
            RelatedItems,
        },
        computed:{
          applicantType: function(){
            return this.proposal.applicant_type;
        },
        },
        methods:{
            set_tabs:function(){
                let vm = this;

                /* set Applicant tab Active */
                $('#pills-tab a[href="#pills-species"]').tab('show');
            },
            eventListener: function(){
              let vm=this;
              $('a[href="#pills-activities-land"]').on('shown.bs.tab', function (e) {
                vm.$refs.activities_land.$refs.vehicles_table.$refs.vehicle_datatable.vmDataTable.columns.adjust().responsive.recalc();
              });
              $('a[href="#pills-activities-marine"]').on('shown.bs.tab', function (e) {
                vm.$refs.activities_marine.$refs.vessel_table.$refs.vessel_datatable.vmDataTable.columns.adjust().responsive.recalc();
              });
            },

        },
        mounted: function() {
            let vm = this;
            vm.set_tabs();
            vm.form = document.forms.new_proposal;
            vm.eventListener();
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

