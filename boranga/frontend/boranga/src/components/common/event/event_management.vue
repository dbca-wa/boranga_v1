<template lang="html">
<div class="row" id="eventManagementInfo">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Event Management <small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#eventManagementInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    <div class="col-sm-12 borderDecoration">
                        
                        <div class="form-group">
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Number of participants expected</label>
                                </div>
                                <div class="col-sm-6">
                                    <input type="number" class="form-control" name="num_participants" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal" v-model="proposal.event_management.num_participants" step="1" onkeydown="return event.keyCode !== 69 && event.keyCode !== 187 && event.keyCode !== 189" @paste.prevent>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Number of spectators expected</label>
                                </div>
                                <div class="col-sm-6">
                                    <input type="number" class="form-control" name="num_spectators" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal" v-model="proposal.event_management.num_spectators" onkeydown="return event.keyCode !== 69 && event.keyCode !== 187 && event.keyCode !== 189" @paste.prevent>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Number of officials</label>
                                </div>
                                <div class="col-sm-6">
                                    <input type="number" class="form-control" name="num_officials" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal" v-model="proposal.event_management.num_officials" onkeydown="return event.keyCode !== 69 && event.keyCode !== 187 && event.keyCode !== 189" @paste.prevent>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Number of vehicles/ vessels</label>
                                </div>
                                <div class="col-sm-6">
                                    <input type="number" class="form-control" name="num_vehicles" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal" v-model="proposal.event_management.num_vehicles" onkeydown="return event.keyCode !== 69 && event.keyCode !== 187 && event.keyCode !== 189" @paste.prevent>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Will the media be involved?</label>                                   
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.media_involved" :value="true" data-parsley-required :disabled="proposal.readonly" name="media_involved"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.media_involved" :value="false" data-parsley-required :disabled="proposal.readonly" name="media_involved"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div v-if="proposal.event_management.media_involved" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Provide details</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea class="form-control" name="off_road_details" placeholder="" v-model="proposal.event_management.media_details" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Will any structures, facilities, signs or markers be erected on CALM land or water for the purpose of the event?</label>                                   
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.structure_change" :value="true" data-parsley-required :disabled="proposal.readonly" name="structure_change"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.structure_change" :value="false" data-parsley-required :disabled="proposal.readonly" name="structure_change"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div v-if="proposal.event_management.structure_change" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Provide details</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea class="form-control" name="structure_change_details" placeholder="" v-model="proposal.event_management.structure_change_details":disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Will food or other supply vendors be hired or contracted to operate on CALM Act land during the event?</label>                                   
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.vendor_hired" :value="true" data-parsley-required :disabled="proposal.readonly" name="vendor_hired"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.vendor_hired" :value="false" data-parsley-required :disabled="proposal.readonly" name="vendor_hired"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div v-if="proposal.event_management.vendor_hired" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Provide details</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea class="form-control" name="vendor_hired_details" placeholder="" v-model="proposal.event_management.vendor_hired_details" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">List any special equipment, facilities or materials required to conduct the proposed activity or event</label>
                                </div>
                                <div class="col-sm-6">
                                      <textarea class="form-control" name="equipment_details" placeholder="" v-model="proposal.event_management.equipment_details" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Will portable toilets and/ or showers be provided?</label>                                   
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.toilets_provided" :value="true" data-parsley-required :disabled="proposal.readonly" name="toilets_provided"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.toilets_provided" :value="false" data-parsley-required :disabled="proposal.readonly" name="toilets_provided"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div v-if="proposal.event_management.toilets_provided" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Provide details</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea class="form-control" name="toilets_provided_details" placeholder="" v-model="proposal.event_management.toilets_provided_details" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <!-- <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Provide the proposed strategy for rubish removal</label>                                   
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.rubbish_removal" :value="true" data-parsley-required :disabled="proposal.readonly" name="rubbish_removal"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.rubbish_removal" :value="false" data-parsley-required :disabled="proposal.readonly" name="rubbish_removal"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div> -->
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Please explain how you will manage waste to avoid impacts on the park/ reserve and remove waste from the park/ reserve following the event</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea class="form-control" name="rubbish_removal_details" placeholder="" v-model="proposal.event_management.rubbish_removal_details" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Have any other agencies, local government representatives, community groups or local committees been consulted and all necessary approvals gained regarding this event?</label>                                   
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.approvals_gained" :value="true" data-parsley-required :disabled="proposal.readonly" name="approvals_gained"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.approvals_gained" :value="false" data-parsley-required :disabled="proposal.readonly" name="approvals_gained"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div v-if="proposal.event_management.approvals_gained" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Provide details</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea class="form-control" name="approvals_gained_details" placeholder="" v-model="proposal.event_management.approvals_gained_details" :disabled="proposal.readonly"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <!-- <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Have you developed emergency response plans and notified the Local Emergency Management Committee(LEMC)? </label>                                   
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.emergency_plan" :value="true" data-parsley-required :disabled="proposal.readonly" name="emergency_plan"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.emergency_plan" :value="false" data-parsley-required :disabled="proposal.readonly" name="emergency_plan"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div class="row" v-if="proposal.event_management.emergency_plan">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Please attach </label>                               
                                </div>
                                <div class="col-sm-6">
                                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="event_management_emergency_plan" :id="'proposal'+proposal.id" :readonly="proposal.readonly"></FileField>
                                </div>                                
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Have you developed an Event Management Plan? </label>                               
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.event_management_plan" :value="true" data-parsley-required :disabled="proposal.readonly" name="event_management_plan"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.event_management_plan" :value="false" data-parsley-required :disabled="proposal.readonly" name="event_management_plan"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div class="row" v-if="proposal.event_management.event_management_plan">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Please attach </label>                               
                                </div>
                                <div class="col-sm-6">
                                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="event_management_event_management_plan" :id="'proposal'+proposal.id" :readonly="proposal.readonly"></FileField>
                                </div>                                
                            </div>
                            <div class="row" v-if="!proposal.event_management.event_management_plan">
                                <div class="col-sm-12">
                                    <label class="control-label pull-left"  for="Name">Please note it will be a condition of any licence approval to provide a copy of your event management plan 30 days prior to conducting your event. </label>                               
                                </div>                               
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Have you developed an Emergency Response Plan? </label>                               
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.emergency_response_plan" :value="true" data-parsley-required :disabled="proposal.readonly" name="emergency_response_plan"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.emergency_response_plan" :value="false" data-parsley-required :disabled="proposal.readonly" name="emergency_response_plan"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div class="row" v-if="proposal.event_management.emergency_response_plan">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Please attach </label>                               
                                </div>
                                <div class="col-sm-6">
                                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="event_management_emergency_response_plan" :id="'proposal'+proposal.id" :readonly="proposal.readonly"></FileField>
                                </div>                                
                            </div>
                            <div class="row" v-if="!proposal.event_management.emergency_response_plan">
                                <div class="col-sm-12">
                                    <label class="control-label pull-left"  for="Name">Please note it will be a condition of any licence approval to provide a copy of your emergency response plan 30 days prior to conducting your event. </label>                               
                                </div>                               
                            </div>



                            <div class="row">&nbsp;</div>
                            <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Have you developed a Risk Management Plan? </label>                                   
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.risk_management_plan" :value="true" data-parsley-required :disabled="proposal.readonly" name="risk_management_plan"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.risk_management_plan" :value="false" data-parsley-required :disabled="proposal.readonly" name="risk_management_plan"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div class="row" v-if="proposal.event_management.risk_management_plan">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Please attach </label>                               
                                </div>
                                <div class="col-sm-6">
                                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="event_management_risk_management_plan" :id="'proposal'+proposal.id" :readonly="proposal.readonly"></FileField>
                                </div>                                
                            </div>
                            <div class="row" v-if="!proposal.event_management.risk_management_plan">
                                <div class="col-sm-12">
                                    <label class="control-label pull-left"  for="Name">Please note it will be a condition of any licence approval to provide a copy of your risk management plan 30 days prior to conducting your event. </label>                               
                                </div>                              
                            </div>
 -->

                            <div class="row">    
                                <div class="col-sm-12">
                                    <label class="control-label pull-left"  for="Name">Please attach a copy of the below listed plans for your event </label>                                   
                                </div>
                            </div>
                            <div class="row">
                               <div class="col-sm-12">
                                    <ul class="list-block"  >
                                        <li class="control-label list-inline-item">
                                            Event Management plan
                                        </li>
                                        <li class="control-label list-inline-item">
                                            Emergency response plan
                                        </li>
                                        <li class="control-label list-inline-item">
                                            Risk Management plan
                                        </li>
                                        
                                    </ul>      
                                </div>
                            </div> 
                            <div class="row">
                                <div class="col-sm-12">
                                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="event_risk_management_plan" :id="'proposal'+proposal.id" :readonly="proposal.readonly" ref="event_risk_management_plan"></FileField>    
                                </div>
                            </div>

                            <div class="row">&nbsp;</div>
                            <div class="row">    
                                <div class="col-sm-6">
                                    <!-- <label class="control-label pull-left"  for="Name">Have you developed a Traffic Management Plan that has been prepared and approved by an accredited body in line with Mainroads WA -  <a :href="event_traffic_code_of_practice" target="_blank">Traffic Management for Events Code of Practice</a>? </label> -->
                                    <label class="control-label pull-left"  for="Name">Does your event route cross or use sections of public road on Conservation and Land Management Act 1984 Land?</label>                                   
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.traffic_management_plan" :value="true" data-parsley-required :disabled="proposal.readonly" name="traffic_management_plan"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_management.traffic_management_plan" :value="false" data-parsley-required :disabled="proposal.readonly" name="traffic_management_plan"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div class="row" v-if="proposal.event_management.traffic_management_plan">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Please attach Traffic Management Plan that has been prepared and approved by an accredited body in line with Mainroads WA -  <a :href="event_traffic_code_of_practice" target="_blank">Traffic Management for Events Code of Practice</a> </label>                               
                                </div>
                                <div class="col-sm-6">
                                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="event_management_traffic_management_plan" :id="'proposal'+proposal.id" :readonly="proposal.readonly" ref="event_management_traffic_management_plan"></FileField>
                                </div>                                
                            </div>
                            <div class="row" v-if="!proposal.event_management.traffic_management_plan">
                                <div class="col-sm-12">
                                    <label class="control-label pull-left"  for="Name">Please note it is a requirement to provide an approved Traffic Management Plan for any event which impacts on public roads.</label>                               
                                </div>
                                                                
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Provide any other information that will be relevant to your application.</label>
                                </div>
                                <div class="col-sm-6">
                                      <textarea class="form-control" name="other_info" placeholder="" v-model="proposal.event_management.other_info" :disabled="proposal.readonly"></textarea>    
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
</template>

<script>
import FileField from '@/components/forms/filefield.vue'
    export default {
        props:{
            proposal:{
                type: Object,
                required:true
            }
        },
        data:function () {
            let vm = this;
            return{
                lBody: 'lBody'+vm._uid,
                values:null,
                global_settings:[],
            }
        },
        components:{
            FileField,
        },
        computed:{
            event_traffic_code_of_practice: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='event_traffic_code_of_practice'){
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
            this.$nextTick(()=>{
                //vm.eventListeners();
            });
        }
    }
</script>

<style lang="css" scoped>
</style>

