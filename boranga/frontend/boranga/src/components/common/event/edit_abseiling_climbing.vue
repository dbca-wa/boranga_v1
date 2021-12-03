<template lang="html">
    <div id="editVehicle">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="abseilingClimbingForm">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <div class="col-sm-12">
                            
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Leader</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <input class="form-control" name="capacity" ref="leader" v-model="abseiling_climbing.leader" type="text">
                                    </div>
                                </div>
                            </div>

                            <!-- <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">NOLARS Registration No.</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <input class="form-control" name="rego" ref="rego" v-model="abseiling_climbing.rego_number" type="text">
                                    </div>
                                </div>
                            </div> -->

                            
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Expiry Date</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div class="input-group date" ref="expiry_date" style="width: 70%;">
                                            <input type="text" class="form-control" name="expiry_date" placeholder="DD/MM/YYYY" v-model="abseiling_climbing.expiry_date">
                                            <span class="input-group-addon">
                                                <span class="glyphicon glyphicon-calendar"></span>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                      
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <button type="button" v-if="issuingRecord" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinner fa-spin"></i> Processing</button>
                <button type="button" v-else class="btn btn-default" @click="ok">Ok</button>
                <button type="button" class="btn btn-default" @click="cancel">Cancel</button>
            </div>
        </modal>
    </div>
</template>

<script>
//import $ from 'jquery'
import Vue from 'vue'
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import {helpers,api_endpoints} from "@/utils/hooks.js"
export default {
    name:'Edit-Vehicle',
    components:{
        modal,
        alert
    },
    props:{
        abseiling_climbing_id: {
            type: Number,
            required: true
        },
        abseiling_climbing_action:{
            type: String,
            default: 'edit'
        },
        
    },
    data:function () {
        let vm = this;
        return {
            isModalOpen:false,
            form:null,
            abseiling_climbing: Object,
            abseiling_climbing_id: Number,
            //access_types: null,
            abseiling_climbing_access_id: null,
            state: 'proposed_abseiling_climbing',
            issuingRecord: false,
            validation_form: null,
            errors: false,
            errorString: '',
            successString: '',
            success:false,
            dateFormat:'YYYY-MM-DD',
            datepickerOptions:{
                format: 'DD/MM/YYYY',
                showClear:true,
                useCurrent:false,
                keepInvalid:true,
                allowInputToggle:true
            },
        }
    },
    computed: {
        showError: function() {
            var vm = this;
            return vm.errors;
        },
        title: function(){
            return this.abseiling_climbing_action == 'add' ? 'Add a new record' : 'Edit a record';
        }
    },
    methods:{
        ok:function () {
            let vm =this;
            if($(vm.form).valid()){
                vm.sendData();
               
            }
        },
        cancel:function () {
            this.close()
        },
        close:function () {
            this.isModalOpen = false;
            this.abseiling_climbing = {};
            this.errors = false;
            $('.has-error').removeClass('has-error');
            $(this.$refs.expiry_date).data('DateTimePicker').clear();
            this.$refs.leader='';
            this.$refs.rego='';
            this.validation_form.resetForm();
        },
        fetchContact: function(id){
            let vm = this;
            vm.$http.get(api_endpoints.contact(id)).then((response) => {
                vm.contact = response.body; vm.isModalOpen = true;
            },(error) => {
                console.log(error);
            } );
        },
        /*
        fetchAccessTypes: function(){
            let vm=this;
            Vue.http.get('/api/access_types.json').then((res) => {
                      vm.access_types=res.body; 
                },
              err => { 
                        console.log(err);
                  });
        },
        */
        fetchRecord: function(vid){
            let vm=this;
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.abseiling_climbing_activities,vid)).then((res) => {
                      vm.abseiling_climbing=res.body; 
                      
                      // if(vm.abseiling_climbing.expiry_date){
                      //   vm.abseiling_climbing.expiry_date=vm.abseiling_climbing.expiry_date.format('DD/MM/YYYY')
                      //   }
                },
              err => { 
                        console.log(err);
                  });
        },

        sendData:function(){
            let vm = this;
            vm.errors = false;
            // if(vm.abseiling_climbing_access_id!=null){
            //     vm.abseiling_climbing.access_type=vm.abseiling_climbing_access_id
            // }
            // if(vm.abseiling_climbing.expiry_date){
            //     vm.abseiling_climbing.expiry_date=vm.abseiling_climbing.expiry_date.format('YYYY-MM-DD')
            // }
            let abseiling_climbing = JSON.parse(JSON.stringify(vm.abseiling_climbing));
            vm.issuingRecord = true;
            if(vm.abseiling_climbing_action=="add" && vm.abseiling_climbing_id==null)
            {
                vm.$http.post(api_endpoints.abseiling_climbing_activities,JSON.stringify(abseiling_climbing),{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.issuingRecord = false;
                        vm.abseiling_climbing={};
                        vm.close();
                        swal(
                             'Created',
                             'New record has been created.',
                             'success'
                        );
                        vm.$emit('refreshFromResponse',response);
                    },(error)=>{
                        vm.errors = true;
                        vm.issuingRecord = false;
                        vm.errorString = helpers.apiVueResourceError(error);
                    });
            }
            else{
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.abseiling_climbing_activities,vm.abseiling_climbing_id+'/edit_abseiling_climbing'),JSON.stringify(abseiling_climbing),{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.issuingRecord = false;
                        vm.abseiling_climbing={};
                        vm.close();
                        swal(
                             'Saved',
                             'Record has been saved.',
                             'success'
                        );
                        vm.$emit('refreshFromResponse',response);
                    },(error)=>{
                        vm.errors = true;
                        vm.issuingRecord = false;
                        vm.errorString = helpers.apiVueResourceError(error);
                    });
                }
        },
        addFormValidations: function() {
            let vm = this;
            vm.validation_form = $(vm.form).validate({
                rules: {
                    //access_type:"required",                    
                },
                messages: {
                },
                showErrors: function(errorMap, errorList) {
                    $.each(this.validElements(), function(index, element) {
                        var $element = $(element);
                        $element.attr("data-original-title", "").parents('.form-group').removeClass('has-error');
                    });
                    // destroy tooltips on valid elements
                    $("." + this.settings.validClass).tooltip("destroy");
                    // add or update tooltips
                    for (var i = 0; i < errorList.length; i++) {
                        var error = errorList[i];
                        $(error.element)
                            .tooltip({
                                trigger: "focus"
                            })
                            .attr("data-original-title", error.message)
                            .parents('.form-group').addClass('has-error');
                    }
                }
            });
       },
       eventListeners:function () {
            let vm = this;
            $(vm.$refs.expiry_date).datetimepicker(vm.datepickerOptions);
            $(vm.$refs.expiry_date).on('dp.change', function(e){
                if ($(vm.$refs.expiry_date).data('DateTimePicker').date()) {
                    vm.abseiling_climbing.expiry_date =  e.date.format('DD/MM/YYYY');
                    //vm.abseiling_climbing.expiry_date =  e.date.format('YYYY-MM-DD')
                }
                else if ($(vm.$refs.expiry_date).data('date') === "") {
                    vm.abseiling_climbing.expiry_date = null;
                }
             });

            // Intialise select2
            // $(vm.$refs.access_type).select2({
            //     "theme": "bootstrap",
            //     allowClear: true,
            //     placeholder:"Select access"
            // }).
            // on("select2:select",function (e) {
            //     var selected = $(e.currentTarget);
            //     //vm.abseiling_climbing.access_type = selected.val();
            //     vm.abseiling_climbing_access_id = selected.val();
            // }).
            // on("select2:unselect",function (e) {
            //     var selected = $(e.currentTarget);
            //     //vm.abseiling_climbing.access_type = selected.val();
            //     vm.abseiling_climbing_access_id = selected.val();
            // });


            //Initialise Date Picker TODO: Check why this is not working
            // console.log($(vm.$refs.expiry_date).datetimepicker(vm.datepickerOptions))
            // $(vm.$refs.expiry_date).datetimepicker(vm.datepickerOptions);
            // $(vm.$refs.expiry_date).on('dp.change', function(e){
            //     if ($(vm.$refs.expiry_date).data('DateTimePicker').date()) {
            //         vm.abseiling_climbing.expiry_date =  e.date.format('DD/MM/YYYY');
            //     }
            //     else if ($(vm.$refs.expiry_date).data('date') === "") {
            //         vm.abseiling_climbing.expiry_date = "";
            //     }
            //  });
       }
   },
   mounted:function () {
        let vm =this;
        //vm.fetchAccessTypes();
        
        vm.form = document.forms.abseilingClimbingForm;
        vm.addFormValidations();
        this.$nextTick(()=>{
            vm.eventListeners();
        });
   }
}
</script>

<style lang="css">
</style>
