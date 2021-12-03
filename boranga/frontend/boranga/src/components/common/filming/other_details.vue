<template lang="html">
<div class="row" id="otherInfo">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Safety<small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#otherInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        
                        <div class="form-group">
                            <div class="row" style="margin-bottom: 5px">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">What steps have been taken to ensure the safety of your filming party? <small> (Provide details of your safety and communication equipment and/or attach a copy of your safety and risk management plan)</small> </label>
                                </div>
                                <div class="col-sm-6">
                                    <div class="input-group date" ref="safety_details" style="width: 70%;">
                                        <textarea type="text" class="form-control" v-model="proposal.filming_other_details.safety_details" name="safety_details" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal"></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="filming_safety_details" :id="'proposal'+proposal.id" :readonly="proposal.readonly"></FileField>
                                </div>                                
                            </div>
                        </div> 
                    </div>
                </div>
            </div>                
        </div>
    </div>
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Other <small></small>
                <a class="panelClicker" :href="'#'+oBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="oBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="oBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                       <div class="form-group">
                           <div class="row">
                                <div class="col-sm-12">
                                    <label>Provide any additional information to support your application. If you would like to access a park that is not listed in the previous sections, please include here.</label>
                                </div>   
                            </div>
                            <div class="row">
                                <div class="col-sm-12" style="margin-bottom: 5px">
                                    <textarea class="form-control" v-model="proposal.filming_other_details.other_comments" :disabled="proposal.readonly"></textarea>
                                </div>                                
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="filming_other_details" :id="'proposal'+proposal.id" :readonly="proposal.readonly"></FileField>
                                </div>                                
                            </div>
                       </div> 
                    </div>
                </div>
            </div>                
        </div>
    </div>


    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Payment of Fees and Charges<small></small>
                <a class="panelClicker" :href="'#'+mBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="mBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="mBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        <div class="form-group">
                            <div class="row">
                                <div class="col-sm-12">
                                    <label>Depending on the filming operation, fees and charges may apply. Please see commercial filming <a :href="fees_and_charges" target="_blank">website</a> for information on fees and charges.</label>
                                </div>   
                            </div>
                            <div class="row">&nbsp;</div>
                            <!-- <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Do you request that camping fees be waived?</label>
                                </div>
                                <div class="col-sm-6" style="margin-bottom: 5px">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                                <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_other_details.camping_fee_waived" :value="true" data-parsley-required :disabled="proposal.readonly" name="camping_fee_waived"/>
                                                Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                                <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_other_details.camping_fee_waived" :value="false" data-parsley-required :disabled="proposal.readonly" name="camping_fee_waived"/>
                                                No
                                        </li>
                                    </ul>
                                </div>
                            </div> -->
                            <div class="row" v-if="proposal.filming_other_details.camping_fee_waived">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">For how many people </label>
                                </div>
                                <div class="col-sm-6" style="margin-bottom: 5px">
                                    <div class="col-sm-6" style="margin-bottom: 5px">
                                        <input type="text" class="form-control" name="num_cameras" placeholder="" :disabled="proposal.readonly" v-model="proposal.filming_other_details.fee_waived_num_people">   
                                    </div>
                                </div>
                            </div>
                            <div class="row" v-if="proposal.filming_other_details.camping_fee_waived">
                                <div class="col-sm-12">
                                    <label class="control-label pull-left"  for="Name">Make sure that you have a copy of the licence or lawful authority if issued. Camping gess  may still apply.</label>
                                </div>
                            </div>
                        </div>
                   </div>
                </div>
            </div>                
        </div>
    </div>
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Insurance <small></small>
                <a class="panelClicker" :href="'#'+iBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="iBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="iBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        <div class="form-group">
                            <div class="row">
                                <div class="col-sm-12">
                                    <label>
                                    <ol type="a">
                                        <li>Attach your policy for public liability insurance that covers the areas and operations allowed under the filming authority, and in the name of the applicant to the extent of its rights and interests, for a sum of not less than AU$10 million per event.</li>
                                        <li>It is a requirement of all filming authority holders to maintain appropriate public liability insurance.</li>
                                    </ol></label>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Certificate of currency
                                    </label>
                                </div>
                                <div class="col-sm-3">
                                    <FileField :proposal_id="proposal.id" isRepeatable="false" name="currency_certificate" :id="'proposal'+proposal.id" :readonly="proposal.readonly" ref="currency_doc"></FileField>
                                </div>
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Expiry Date
                                    </label>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group date" ref="insurance_expiry" style="width: 70%;">
                                        <input type="text" class="form-control" name="insurance_expiry" placeholder="DD/MM/YYYY" v-model="proposal.filming_other_details.insurance_expiry" :disabled="proposal.readonly">
                                            <span class="input-group-addon">
                                                <span class="glyphicon glyphicon-calendar"></span>
                                            </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>                
        </div>
    </div>
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Deed Poll<small></small>
                <a class="panelClicker" :href="'#'+dBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="dBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="dBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        <div class="form-group">
                           <div class="row">
                                <div class="col-sm-12">
                                    <label>It is a requirement of all filming authority holders to sign a deed poll to release and indemnify the State of Western Australia. Please note: electronic or digital signatures cannot be accepted.</label>
                                    <label v-if="deed_poll_url">Please click <a :href="deed_poll_url" target="_blank">here</a> to download the deed poll. The deed poll must be signed and have a witness signature and be dated. Once signed and dated, please scan and attach the deed poll below.</label>
                                    <label v-else>Please click here to download the deed poll. The deed poll must be signed and have a witness signature and be dated. Once signed and dated, please scan and attach the deed poll below.</label>
                                </div>   
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <FileField :proposal_id="proposal.id" isRepeatable="false" name="deed_poll" :id="'proposal'+proposal.id" :readonly="proposal.readonly" ref="deed_poll_doc"></FileField>
                                </div>                                
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
import Vue from 'vue' 
//import Accreditation from './accreditation_type.vue'
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
            }
        },
        data:function () {
            let vm = this;
            return{
                pBody: 'pBody'+vm._uid,
                lBody: 'lBody'+vm._uid,
                iBody: 'iBody'+vm._uid,
                mBody: 'mBody'+vm._uid,
                oBody: 'oBody'+vm._uid,
                cBody: 'cBody'+vm._uid,
                dBody: 'dBody'+vm._uid,
                values:null,
                global_settings:[],
                //mooring:[{'value':''}],
                datepickerOptions:{
                    format: 'DD/MM/YYYY',
                    showClear:true,
                    useCurrent:false,
                    keepInvalid:true,
                    allowInputToggle:true,
                },
            }
        },
        components: {
          FileField,
          //Accreditation
        },
        computed: {
            deed_poll_url: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='deed_poll_filming'){
                            return vm.global_settings[i].value;
                        }
                    }
                }
                return '';
            },
            credit_facility_link: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='credit_facility_link'){
                            return vm.global_settings[i].value;
                        }
                    }
                }
                return '';
            },
            fees_and_charges: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='fees_and_charges'){
                            return vm.global_settings[i].value;
                        }
                    }
                }
                return '';
            }
        },
        watch:{
            
            
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
            
            eventListeners:function (){
                let vm=this;

                var date= new Date()
                var today= new Date(date.getFullYear(), date.getMonth(), date.getDate());

                 
                //Insurance expiry date listener
                $(vm.$refs.insurance_expiry).datetimepicker(vm.datepickerOptions);
                //Set minimum date on datetimepicker so that
                //insurance expiry date cannot be selected prior to today
                $(vm.$refs.insurance_expiry).data("DateTimePicker").minDate(today);
                $(vm.$refs.insurance_expiry).on('dp.change', function(e){
                    if ($(vm.$refs.insurance_expiry).data('DateTimePicker').date()) {                       
                        vm.proposal.filming_other_details.insurance_expiry =  e.date.format('DD/MM/YYYY');
                    }
                    else if ($(vm.$refs.insurance_expiry).data('date') === "") {
                        vm.proposal.filming_other_details.insurance_expiry = "";
                    }
                 });
                

                
            },
        },
        mounted: function(){
            let vm = this;
            vm.fetchGlobalSettings();
            this.$nextTick(()=>{
                vm.eventListeners();
            });
        }
    }
</script>

<style lang="css" scoped>
    /*ul, li {
        zoom:1;
        display: inline;
    }*/
    fieldset.scheduler-border {
    border: 1px groove #ddd !important;
    padding: 0 1.4em 1.4em 1.4em !important;
    margin: 0 0 1.5em 0 !important;
    -webkit-box-shadow:  0px 0px 0px 0px #000;
            box-shadow:  0px 0px 0px 0px #000;
    }
    legend.scheduler-border {
    width:inherit; /* Or auto */
    padding:0 10px; /* To give a bit of padding on the left and right */
    border-bottom:none;
    }
</style>

