<template lang="html">
    <div id="editPark">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="parkForm">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Park or Reserve</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <select class="form-control" name="park" ref="events_park" @change="fetchAllowedActivities" v-model="events_park_id">
                                            <option v-for="p in parks_list" :value="p.id">{{p.name}}</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Activity Types (application)</label>
                                    </div>
                                    <!-- <div class="col-sm-9" v-if="">
                                        <select style="width:100%" class="form-control input-sm" multiple ref="activities_select" v-model="selected_activities">
                                            <option v-for="a in allowed_activities" :value="a.id">{{a.name}}</option>
                                        </select>
                                    </div> -->

                                    <div class="col-sm-9" v-if="">
                                        
                                        <input type="text" class="form-control" name="pre_event_name"  v-model="park.event_activities" :readonly="is_internal">
                                    </div>

                                </div>
                            </div>
                            <div class="form-group" v-if="is_internal">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Activity Types (assessor)</label>
                                    </div>
                                    <div class="col-sm-9" v-if="">
                                        <select style="width:100%" class="form-control input-sm" multiple ref="activities_select" v-model="selected_activities">
                                            <option v-for="a in park_activities" :value="a.id">{{a.name}}</option>
                                        </select>
                                    </div>

                                    <!-- <div class="col-sm-9" v-if="">
                                        
                                        <input type="text" class="form-control" name="pre_event_name"  v-model="park.event_activities">
                                    </div> -->

                                </div>
                            </div>

                           
                           

                            <!-- <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Maps/ Documents</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div class="input-group date" ref="add_attachments" style="width: 70%;">
                                            <FileField2 ref="filefield" :uploaded_documents="park.events_park_documents" :delete_url="delete_url" :proposal_id="park_id" isRepeatable="true" name="events_park_file" @refreshFromResponse="refreshFromResponse"/>
                                        </div>

                                    </div>
                                </div>
                            </div> -->
                                                     
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <button type="button" v-if="issuingPark" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinner fa-spin"></i> Processing</button>
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
import FileField2 from '@/components/forms/filefield2.vue'
export default {
    name:'Edit-Park-Activity',
    components:{
        modal,
        alert,
        FileField2
    },
    props:{
        is_internal:{
              type: Boolean,
              default: false
        },
        park_id: {
            type: Number,
            required: true
        },
        park_action:{
            type: String,
            default: 'edit'
        },
        is_external:{
              type: Boolean,
              default: false
        },
    },
    data:function () {
        let vm = this;
        return {
            isModalOpen:false,
            form:null,
            park: Object,
            park_id: Number,
            events_park_id:Number,
            //access_types: null,
            state: 'proposed_park',
            issuingPark: false,
            parks_list:[],
            park_activities:[],
            selected_activities:[],
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
            return this.park_action == 'add' ? 'Add a new Park or Reserve' : 'Edit a Park or Reserve';
        },
        delete_url: function() {
            return (this.park_id) ? '/api/proposal_events_parks/'+this.park_id+'/delete_document/' : '';
        }
    },
    methods:{
        refreshFromResponse: function(updated_docs){
            this.park.events_park_documents = updated_docs;
        },
        ok:function () {
            let vm =this;
            if($(vm.form).valid()){
                vm.sendData();
               //vm.$refs.filefield.reset_files();
            }
        },
        cancel:function () {
            this.close()
            this.$refs.filefield.reset_files();
        },
        close:function () {
            this.isModalOpen = false;
            this.park = {};
            //this.$refs.filefield.reset_files();
            this.errors = false;
            $('.has-error').removeClass('has-error');
            //this.$refs.activities_select=[];
            $(this.$refs.activities_select).val(null).trigger('change');
            //this.events_park_id=null;
            $(this.$refs.events_park).val(null).trigger('change');
            this.selected_activities=[];
            this.events_park_id=null;
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
        fetchAllParks_orig: function(id){
            let vm = this;
            vm.$http.get(api_endpoints.event_park_container).then((response) => {
                vm.parks_list = response.body; 
            },(error) => {
                console.log(error);
            } );
        },
        fetchAllParks: function(id){
            let vm = this;
            vm.$http.get(api_endpoints.event_park_container).then((response) => {
                //vm.parks_list = response.body['parks'];
                if(vm.is_external){
                    vm.parks_list = response.body['parks_external'];
                }
                else{
                    vm.parks_list = response.body['parks'];
                }
                vm.park_activities=response.body['event_activity_types'];
            },(error) => {
                console.log(error);
            } );
        },

        fetchActivities: function(id){
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.parks,'land_parks')).then((response) => {
                vm.land_parks = response.body; 
            },(error) => {
                console.log(error);
            } );
        },
        
        fetchPark: function(vid){
            let vm=this;
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.proposal_events_parks,vid)).then((res) => {
                      vm.park=res.body; 
                      if(vm.park.park)
                      {
                        vm.events_park_id=vm.park.park.id
                        // $(vm.$refs.events_park).val(vm.events_park_id)
                        // $(vm.$refs.events_park).trigger('change')
                        $(vm.$refs.events_park).val(vm.park.park.id).trigger('change');
                        //vm.fetchAllowedActivities();
                      }
                      if(vm.park.activities_assessor)
                      {
                        vm.selected_activities=vm.park.activities_assessor;
                        $(vm.$refs.activities_select).val(vm.park.activities_assessor).trigger('change');
                      }
                      // if(vm.park.from_date){
                      //   vm.park.from_date=vm.park.from_date.format('DD/MM/YYYY')
                      //   }
                },
              err => { 
                        console.log(err);
                  });
        },
        fetchAllowedActivities: function(){
            /* Searches for dictionary in list */
            console.log('here');
            let vm=this;
            for (var i = 0; i < vm.parks_list.length; i++) {
                if (vm.parks_list[i].id == vm.events_park_id) {
                    vm.allowed_activities = vm.parks_list[i].allowed_activities;
                }
            }
            $(vm.$refs.activities_select).trigger('change');
        },
        sendData:function(){
            let vm = this;
            vm.errors = false;
            if(vm.events_park_id!=null){
                vm.park.park=vm.events_park_id
            }
            vm.park.activities_assessor = vm.selected_activities;
            // if(vm.park.from_date){
            //     vm.park.from_date=vm.park.from_date.format('YYYY-MM-DD')
            // }
            let park = JSON.parse(JSON.stringify(vm.park));
            let formData = new FormData()
            //original append file code
            // var files = vm.$refs.filefield.files;
            // $.each(files, function (idx, v) {
            //     var file = v['file'];
            //     var filename = v['name'];
            //     var name = 'file-' + idx;
            //     formData.append(name, file, filename);
            // });
            // park.num_files = files.length;
            // park.input_name = 'events_park_doc';
            //end append file code
            //park.proposal = vm.proposal_id;

            formData.append('data', JSON.stringify(park));
            //let park = JSON.parse(JSON.stringify(vm.park));
            vm.issuingPark = true;
            if(vm.park_action=="add" && vm.park_id==null)
            {
                vm.$http.post(api_endpoints.proposal_events_parks,formData,{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.issuingPark = false;
                        vm.park={};
                        vm.close();
                        swal(
                             'Created',
                             'New park record has been created.',
                             'success'
                        );
                        vm.$emit('refreshFromResponse',response);
                    },(error)=>{
                        vm.errors = true;
                        vm.issuingPark = false;
                        vm.errorString = helpers.apiVueResourceError(error);
                    });
            }
            else{
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.proposal_events_parks,vm.park_id+'/edit_park'),formData,{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.issuingPark = false;
                        vm.park={};
                        vm.close();
                        swal(
                             'Saved',
                             'Park details has been saved.',
                             'success'
                        );
                        vm.$emit('refreshFromResponse',response);
                    },(error)=>{
                        vm.errors = true;
                        vm.issuingPark = false;
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
            $(vm.$refs.events_park).select2({
                "theme": "bootstrap",
                allowClear: true,
                placeholder:"Select Park"
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                vm.events_park_id = selected.val();
                //vm.fetchAllowedActivities();
            }).
            on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                vm.events_park_id = selected.val();
                //vm.fetchAllowedActivities();
            });
            // Initialise select2 for Activity types
                $(vm.$refs.activities_select).select2({
                    "theme": "bootstrap",
                    allowClear: true,
                    placeholder:"Select Activities"
                }).
                on("select2:select",function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_activities = selected.val();
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_activities = selected.val();
                });
            
       }
   },
   mounted:function () {
        let vm =this;
        //vm.fetchAccessTypes();
        vm.fetchAllParks();
        vm.form = document.forms.parkForm;
        vm.addFormValidations();
        this.$nextTick(()=>{
            vm.eventListeners();
        });
        //vm.park.events_park_documents = vm.$refs.filefield.uploaded_documents;
   }
}
</script>

<style lang="css">
</style>
