<template lang="html">
<div class="row" id="accessInfo">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Access Requirements <small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#accessInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        
                        <div class="form-group">
                            <div class="">
                                
                                <div class="col-sm-12">
                                    <label class="text-left"  for="Name">Please list which parks (terrestrial and/or marine) you wish to access. If accessing multiple areas of Western Australia, please list all parks. Visit <a :href="park_finder_link" target="_blank">here</a> for assistance with identifying your required parks.</label>
                                    <ParkTable :url="parks_url" :proposal="proposal"  ref="parks_table" :hasDistrictAssessorMode="hasDistrictAssessorMode" :district_proposal= "district_proposal" :canEditActivities="canEditActivities" :is_external= "is_external"></ParkTable>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                        </div> 
                    </div>

                    <div class="col-sm-12 borderDecoration">
                        
                        <div class="form-group">
                            <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Do you intend to use the Munda Biddi or Bibbulmun Track?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.track_use" :value="true" data-parsley-required :disabled="proposal.readonly" name="track_use"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.track_use" :value="false" data-parsley-required :disabled="proposal.readonly" name="track_use"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div v-if="proposal.filming_access.track_use" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Please provide details </label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="track_use_details" placeholder="" v-model="proposal.filming_access.track_use_details" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Do you intend to conduct any off-road/ track driving/ walking?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.off_road" :value="true" data-parsley-required :disabled="proposal.readonly" name="off_road"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.off_road" :value="false" data-parsley-required :disabled="proposal.readonly" name="off_road"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.off_road" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Please provide details </label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="off_road_details" placeholder="" v-model="proposal.filming_access.off_road_details" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Do you require roads or car parks to be closed during filming?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.road_closure" :value="true" data-parsley-required :disabled="proposal.readonly" name="road_closure"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.road_closure" :value="false" data-parsley-required :disabled="proposal.readonly" name="road_closure"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.road_closure" class="row" >
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Please provide details </label>
                                    
                                </div>
                                <div class="col-sm-6" style="margin-bottom: 5px !important">
                                      <textarea :disabled="readonly" class="form-control" name="road_closure_details" placeholder="" v-model="proposal.filming_access.road_closure_details" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div  class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Number of people in filming party</label>
                                    
                                </div>
                                <div class="col-sm-6" style="margin-bottom: 5px">
                                      <input type="text" class="form-control" name="no_of_people" placeholder="" :disabled="proposal.readonly" v-model="proposal.filming_access.no_of_people">   
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                     Do you intend to camp on CALM Act Land? (Camping fees apply as per normal public charges. Campgrounds may be bookable on the <a :href="park_stay_link" target="_blank">Park Stay WA</a> website)</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.camp_on_land" :value="true" data-parsley-required :disabled="proposal.readonly" name="camp_on_land"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.camp_on_land" :value="false" data-parsley-required :disabled="proposal.readonly" name="camp_on_land"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.camp_on_land" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Where?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="camp_location" placeholder="" v-model="proposal.filming_access.camp_location" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Will you need assistance from Department staff? <small> (Supervision fees may apply)</small> </label>
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.staff_assistance" :value="true" data-parsley-required :disabled="proposal.readonly" name="staff_assistance"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.staff_assistance" :value="false" data-parsley-required :disabled="proposal.readonly" name="staff_assistance"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.staff_assistance" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    In what capacity and for how long?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="camp_location" placeholder="" v-model="proposal.filming_access.assistance_staff_capacity" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Will you need Department staff to Film? <small> (Supervision fees may apply)</small> </label>
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.staff_to_film" :value="true" data-parsley-required :disabled="proposal.readonly" name="staff_to_film"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.staff_to_film" :value="false" data-parsley-required :disabled="proposal.readonly" name="staff_to_film"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.staff_to_film" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    In what capacity and for how long?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="camp_location" placeholder="" v-model="proposal.filming_access.film_staff_capacity" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Will you be featuring Aboriginal people/ items/ area of cultural significance?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.cultural_significance" :value="true" data-parsley-required :disabled="proposal.readonly" name="cultural_significance"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.cultural_significance" :value="false" data-parsley-required :disabled="proposal.readonly" name="cultural_significance"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.cultural_significance" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Please advise how you propose to depict Aboriginal people or items/areas of cultural significance </label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="camp_location" placeholder="" v-model="proposal.filming_access.cultural_significance_details" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row" v-if="proposal.filming_access.cultural_significance">
                                
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    If applicable, please upload a copy of your written approval from the relevant Aboriginal traditional owner group for filming at Aboriginal cultural sites or filming of cultural material. Please see the Commercial Filming Handbook <a :href="commercial_filming_handbook" target="_blank">here</a> for information on required approvals and contact details </label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="cultural_significance" :id="'proposal'+proposal.id" :readonly="proposal.readonly"></FileField>
                                </div>                                
                            </div>
                            
                            <div class="row">&nbsp;</div>
                        </div>
                    </div> 
                </div>

                </div>
            </div>                

        </div>
    </div>

</div>
</template>

<script>
import ParkTable from './parks_table.vue'
import FileField from '@/components/forms/filefield.vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
    export default {
        props:{
            proposal:{
                type: Object,
                required:true
            },
            hasDistrictAssessorMode:{
                type:Boolean,
                default: false
            },
            district_proposal:{
                type:Object,
                default:null
            },
            canEditActivities:{
              type: Boolean,
              default: true
            },
            is_external:{
              type: Boolean,
              default: false
            },
            canEditPeriod:{
              type: Boolean,
              default: false
            },
        },
        data:function () {
            let vm = this;
            return{
                lBody: 'lBody'+vm._uid,
                values:null,
                parks_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.proposal_id+'/filming_parks'),
                global_settings:[],
            }
        },
        components:{
            ParkTable,
            FileField
        },
        computed: {
            park_finder_link: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='park_finder_link'){
                            return vm.global_settings[i].value;
                        }
                    }
                }
                return '';
            },
            commercial_filming_handbook: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='commercial_filming_handbook'){
                            return vm.global_settings[i].value;
                        }
                    }
                }
                return '';
            },
            park_stay_link: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='park_stay_link'){
                            return vm.global_settings[i].value;
                        }
                    }
                }
                return '';
            },
            
        },
        methods:{
            fetchGlobalSettings: function(){
                let vm = this;
                vm.$http.get('/api/global_settings.json').then((response) => {
                    vm.global_settings = response.body;
                    
                },(error) => {
                    console.log(error);
                } );
            },
        },
        mounted: function(){
            let vm = this;
            vm.fetchGlobalSettings();
        }
    }
</script>

<style lang="css" scoped>
.borderDecoration {
    border: 1px solid;
    border-radius: 5px;
    padding: 5px;
    margin-top: 5px;
}
</style>

