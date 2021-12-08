<template lang="html">
<div class="row" id="userInfo">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Documents <small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        
                        <div class="form-group">
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Some documents data</label>
                                </div>
                                <div class="col-sm-9" style="margin-bottom: 5px; width:53% !important">
                                    <input type="text" class="form-control" name="Some species data" placeholder="" :disabled="proposal.readonly" v-model="some_documents_data">
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
                accreditation_choices:[],
                accreditation_type:[],
                selected_accreditations:[],
                licence_period_choices:[],
                mooring: [''],
                global_settings:[],
                //mooring:[{'value':''}],
                datepickerOptions:{
                format: 'DD/MM/YYYY',
                showClear:true,
                useCurrent:false,
                keepInvalid:true,
                allowInputToggle:true,
                some_documents_data: null,
            },
            }
        },
        components: {
        },
        computed: {
            deed_poll_url: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='deed_poll'){
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
            }
        },
        watch:{
            
            accreditation_type: function(){
                this.proposal.other_details.accreditation_type=this.accreditation_type.key;
            },
        },
        methods:{
            handleRadioChange: function(e){
                    if(e.target.value=="true"){
                        console.log(e.target.value);
                        $('#show_docket').removeClass('hidden')
                    }
                    else{
                        $('#show_docket').addClass('hidden')
                    }
                
            },
            handleSelectionChange: function(e){
                    if(e.target.value=="true"){
                        console.log(e.target.value);
                        $('#show_credit_link').removeClass('hidden')
                    }
                    else{
                        $('#show_credit_link').addClass('hidden')
                    }
                
            },
            showDockteNumber: function(){
                let vm=this;
                if(vm.proposal && vm.proposal.other_details.credit_docket_books){
                    var input = this.$refs.docket_books_yes;
                    var e = document.createEvent('HTMLEvents');
                    e.initEvent('change', true, true);
                    var disabledStatus = input.disabled;
                    try {
                        /* Firefox will not fire events for disabled widgets, so (temporarily) enabling them */
                        if(disabledStatus) {
                            input.disabled = false;
                        }
                        input.dispatchEvent(e);
                    } finally {
                        if(disabledStatus) {
                            input.disabled = true;
                        }
                    }
                }
            },
            showCreditFacilityLink: function(){
                let vm=this;
                if(vm.proposal && vm.proposal.other_details.credit_fees){
                    var input = this.$refs.credit_fees_yes;
                    var e = document.createEvent('HTMLEvents');
                    e.initEvent('change', true, true);
                    var disabledStatus = input.disabled;
                    try {
                        /* Firefox will not fire events for disabled widgets, so (temporarily) enabling them */
                        if(disabledStatus) {
                            input.disabled = false;
                        }
                        input.dispatchEvent(e);
                    } finally {
                        if(disabledStatus) {
                            input.disabled = true;
                        }
                    }
                }
            },
            addMooring: function(){
                let vm=this;
                //var new_mooring= helpers.copyObject(vm.mooring)
                var new_mooring= helpers.copyObject(vm.proposal.other_details.mooring)
                new_mooring.push('');
                vm.proposal.other_details.mooring=new_mooring;
                console.log(vm.proposal.other_details.mooring);
            },
            fetchAccreditationChoices: function(){
                let vm = this;
                vm.$http.get('/api/accreditation_choices.json').then((response) => {
                    vm.accreditation_choices = response.body;
                    if(vm.proposal.other_details.accreditation_type
                        ){
                        for(var i=0; i<vm.accreditation_choices.length; i++){
                            if(vm.accreditation_choices[i].key==vm.proposal.other_details.accreditation_type){
                                vm.accreditation_type=vm.accreditation_choices[i]
                            }
                        }
                    }
                    
                },(error) => {
                    console.log(error);
                } );
            },
            fetchLicencePeriodChoices: function(){
                let vm = this;
                vm.$http.get('/api/licence_period_choices.json').then((response) => {
                    vm.licence_period_choices = response.body;
                    
                },(error) => {
                    console.log(error);
                } );
            },
            fetchGlobalSettings: function(){
                let vm = this;
                vm.$http.get('/api/global_settings.json').then((response) => {
                    vm.global_settings = response.body;
                    
                },(error) => {
                    console.log(error);
                } );
            },
            checkProposalAccreditation: function(){
                let vm= this;
                if(vm.proposal && vm.proposal.other_details){
                    for(var i=0; i<vm.proposal.other_details.accreditations.length; i++){
                        vm.proposal.other_details.accreditations[i].is_deleted=false;
                        vm.selected_accreditations.push(vm.proposal.other_details.accreditations[i].accreditation_type);
                    }
                }
            },
            selectAccreditation: function(e, accreditation_type){
                let vm=this;
                if(e.target.checked){
                    var found=false;
                    for(var i=0;i<vm.proposal.other_details.accreditations.length; i++){
                        if(vm.proposal.other_details.accreditations[i].accreditation_type==accreditation_type.key){
                            found=true;
                            vm.proposal.other_details.accreditations[i].is_deleted=false;
                        }
                    }
                    if(found==false){
                    var data={
                        'accreditation_type': accreditation_type.key,
                        'accreditation_expiry':null,
                        'comments':'',
                        'proposal_other_details': vm.proposal.other_details.id,
                        'is_deleted': false,
                        'accreditation_type_value': accreditation_type.value
                    }
                    var acc=helpers.copyObject(vm.proposal.other_details.accreditations);
                    acc.push(data);
                    vm.proposal.other_details.accreditations=acc;
                    }
                }
                else{
                    for(var i=0;i<vm.proposal.other_details.accreditations.length; i++)
                    {

                        if(vm.proposal.other_details.accreditations[i].accreditation_type==accreditation_type.key)
                        {
                            if(vm.proposal.other_details.accreditations[i].id){
                                //console.log('yes')
                                var acc=helpers.copyObject(vm.proposal.other_details.accreditations);
                                acc[i].is_deleted=true;
                                vm.proposal.other_details.accreditations=acc;
                            }
                            else{
                                var acc=helpers.copyObject(vm.proposal.other_details.accreditations);
                                acc.splice(i,1);
                                vm.proposal.other_details.accreditations=acc;
                            }
                        }
                    }
                }
            },
            eventListeners:function (){
                let vm=this;

                var date= new Date()
                var today= new Date(date.getFullYear(), date.getMonth(), date.getDate());

                $(vm.$refs.accreditation_expiry).datetimepicker(vm.datepickerOptions);
                $(vm.$refs.accreditation_expiry).on('dp.change', function(e){
                    if ($(vm.$refs.accreditation_expiry).data('DateTimePicker').date()) {
                        

                        vm.proposal.other_details.accreditation_expiry =  e.date.format('DD/MM/YYYY');
                    }
                    else if ($(vm.$refs.accreditation_expiry).data('date') === "") {
                        vm.proposal.other_details.accreditation_expiry = "";
                    }
                 });
                //Nominated start date listener
                $(vm.$refs.nominated_start_date).datetimepicker(vm.datepickerOptions);
                //Set minimum date on datetimepicker so that nominated
                //start date cannot be selected prior to today
                $(vm.$refs.nominated_start_date).data("DateTimePicker").minDate(today);
                $(vm.$refs.nominated_start_date).on('dp.change', function(e){
                    if ($(vm.$refs.nominated_start_date).data('DateTimePicker').date()) {
                        

                        vm.proposal.other_details.nominated_start_date =  e.date.format('DD/MM/YYYY');
                    }
                    else if ($(vm.$refs.nominated_start_date).data('date') === "") {
                        vm.proposal.other_details.nominated_start_date = "";
                    }
                 });
                //Insurance expiry date listener
                $(vm.$refs.insurance_expiry).datetimepicker(vm.datepickerOptions);
                //Set minimum date on datetimepicker so that
                //insurance expiry date cannot be selected prior to today
                $(vm.$refs.insurance_expiry).data("DateTimePicker").minDate(today);
                $(vm.$refs.insurance_expiry).on('dp.change', function(e){
                    if ($(vm.$refs.insurance_expiry).data('DateTimePicker').date()) {                       

                        vm.proposal.other_details.insurance_expiry =  e.date.format('DD/MM/YYYY');
                    }
                    else if ($(vm.$refs.insurance_expiry).data('date') === "") {
                        vm.proposal.other_details.insurance_expiry = "";
                    }
                 });
                // Intialise select2
                $(vm.$refs.preferred_licence_period).select2({
                    "theme": "bootstrap",
                    allowClear: true,
                    placeholder:"Select preferred licence term"
                }).
                on("select2:select",function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.other_details.preferred_licence_period = selected.val();
                    vm.proposal.other_details.preferred_licence_period_id = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.other_details.preferred_licence_period = selected.val();
                    vm.proposal.other_details.preferred_licence_period_id = selected.val();
                });
            },
        },
        mounted: function(){
            let vm = this;
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

