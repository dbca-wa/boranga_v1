<template lang="html">
    <div id="editEventTrailSection2">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="parkForm">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Trail</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <select class="form-control" name="event_trail_new" ref="events_trail" v-model="events_trail_id">
                                            <option v-for="t in trails_list" :value="t.id" v-bind:key="t.id">{{t.name}}</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <!-- <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Sections</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <select class="form-control" name="section" ref="events_section" v-model="section_id">
                                            <option v-for="s in section_list" :value="s.id">{{s.name}}</option>
                                        </select>
                                    </div>
                                </div>
                            </div> -->
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Sections</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <select class="form-control" name="event_trail_section" ref="events_section" v-model="section_id">
                                            <option v-for="s in trail_list_filter" :value="s.id" v-bind:key="s.id">{{s.name}}</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Activity Types</label>
                                    </div>
                                    <!-- <div class="col-sm-9" v-if="">
                                        <select style="width:100%" class="form-control input-sm" multiple ref="activities_select" v-model="selected_activities">
                                            <option v-for="a in trail_activities" :value="a.id">{{a.name}}</option>
                                        </select>
                                    </div> -->

                                    <div class="col-sm-9" v-if="">
                                        
                                        <input type="text" class="form-control" name="pre_event_name"  v-model="trail.event_trail_activities" :readonly="is_internal">
                                    </div>

                                </div>
                            </div>

                            <div class="form-group" v-if="is_internal">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Activity Types (internal) </label>
                                    </div>
                                    <div class="col-sm-9" v-if="">
                                        <select style="width:100%" class="form-control input-sm" multiple ref="activities_select" v-model="selected_activities">
                                            <option v-for="a in trail_activities" :value="a.id">{{a.name}}</option>
                                        </select>
                                    </div>


                                </div>
                            </div>

                           
                           

                            <!-- <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        
                                        <label class="control-label pull-left"  for="Name">Maps/ Documents</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div class="input-group date" ref="add_attachments" style="width: 70%;">
                                            <FileField2 ref="filefield" :uploaded_documents="park.events_trail_documents" :delete_url="delete_url" :proposal_id="park_id" isRepeatable="true" name="events_trail_file" @refreshFromResponse="refreshFromResponse"/>
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
    name:'Edit-Trail-Activity-Event',
    components:{
        modal,
        alert,
        FileField2
    },
    props:{
        // level:{
        //     type: String,
        //     required: true,
        //     validator:function(val) {
        //         let options = ['internal','referral','external'];
        //         return options.indexOf(val) != -1 ? true: false;
        //     }
        // },
        is_internal:{
              type: Boolean,
              default: false
        },
        trail_id: {
            type: Number,
            required: true
        },
        trail_action:{
            type: String,
            default: 'edit'
        },
    },
    data:function () {
        let vm = this;
        return {
            isModalOpen:false,
            form:null,
            trail: Object,
            trail_id: Number,
            section_id: Number,
            events_trail_id:Number,
            //access_types: null,
            state: 'proposed_park',
            issuingPark: false,
            trails_list:[],
            section_list:[],
            trail_activities:[],
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
            return this.park_action == 'add' ? 'Add a new Trail' : 'Edit a Trail';
        },
        delete_url: function() {
            return (this.park_id) ? '/api/proposal_events_trails/'+this.park_id+'/delete_document/' : '';
        },
        trail_list_filter:function(){
            let trail_list=[];
            var vm = this;
            for (var i = 0; i < vm.trails_list.length; i++) {
                if (vm.trails_list[i].id == vm.events_trail_id) {
                    //vm.section_list = vm.trails_list[i].sections;
                    //vm.section_list = helpers.copyObject(vm.trails_list[i].sections)
                    return vm.trails_list[i].sections;
                }
            }
        }

    },
    methods:{
        refreshFromResponse: function(updated_docs){
            this.park.events_trail_documents = updated_docs;
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
            //this.$refs.filefield.reset_files();
        },
        close:function () {
            this.isModalOpen = false;
            this.trail = {};
            //this.$refs.filefield.reset_files();
            this.errors = false;
            $('.has-error').removeClass('has-error');
            //this.$refs.activities_select=[];
            $(this.$refs.activities_select).val(null).trigger('change');
            //this.events_trail_id=null;
            $(this.$refs.events_trail).val(null).trigger('change');
            $(this.$refs.events_section).val(null).trigger('change');
            this.selected_activities=[];
            this.section_list=[];
            this.events_trail_id=null;
            this.section_id=null;
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
        
        fetchAllTrails_orig: function(id){
            let vm = this;
            vm.$http.get(api_endpoints.trails).then((response) => {
                vm.trails_list = response.body; 

            },(error) => {
                console.log(error);
            } );
        },
        fetchAllTrails: function(id){
            let vm = this;
            vm.$http.get(api_endpoints.event_trail_container).then((response) => {
                vm.trails_list = response.body['trails'];
                vm.trail_activities= response.body['event_activity_types'] 

            },(error) => {
                console.log(error);
            } );
        },

        
        fetchTrail: function(vid){
            let vm=this;
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.proposal_events_trails,vid)).then((res) => {
                      vm.trail=res.body; 
                      if(vm.trail.trail)
                      {
                        vm.events_trail_id=vm.trail.trail.id
                        if(vm.trail.section){
                            vm.section_id=vm.trail.section.id
                        }
                        
                        // $(vm.$refs.events_trail).val(vm.events_trail_id)
                        // $(vm.$refs.events_trail).trigger('change')
                        $(vm.$refs.events_trail).val(vm.trail.trail.id).trigger('change');
                        vm.fetchSections();
                        if(vm.trail.section){
                            $(vm.$refs.events_section).val(vm.trail.section.id).trigger('change');
                        }
                        
                        // vm.fetchSections();
                      }
                      if(vm.trail.activities_assessor)
                      {
                        vm.selected_activities=vm.trail.activities_assessor;
                        $(vm.$refs.activities_select).val(vm.trail.activities_assessor).trigger('change');
                      }
                      // if(vm.trail.from_date){
                      //   vm.trail.from_date=vm.trail.from_date.format('DD/MM/YYYY')
                      //   }
                },
              err => { 
                        console.log(err);
                  });
        },
        
        fetchSections: function(){
            /* Searches for dictionary in list */
            //console.log('here');
            let vm=this;
            vm.section_list=[];
            $(this.$refs.events_section).val(null).trigger('change');
            for (var i = 0; i < vm.trails_list.length; i++) {
                if (vm.trails_list[i].id == vm.events_trail_id) {
                    //vm.section_list = vm.trails_list[i].sections;
                    vm.section_list = helpers.copyObject(vm.trails_list[i].sections)
                }
            }
            //console.log(vm.section_list);
            $(vm.$refs.events_section).val(vm.section_list).trigger('change');
        },
        sendData:function(){
            let vm = this;
            vm.errors = false;
            if(vm.events_trail_id!=null){
                vm.trail.trail=vm.events_trail_id
            }
            //console.log('section_id',vm.section_id);
            if(vm.section_id!=null){
                vm.trail.section=vm.section_id
            }
            //console.log('trail.section',vm.trail.section);
            vm.trail.activities_assessor = vm.selected_activities;
            //console.log(vm.trail.activities_assessor);
            // if(vm.trail.from_date){
            //     vm.trail.from_date=vm.trail.from_date.format('YYYY-MM-DD')
            // }
            let trail = JSON.parse(JSON.stringify(vm.trail));
            let formData = new FormData()
            //original append file code
            // var files = vm.$refs.filefield.files;
            // $.each(files, function (idx, v) {
            //     var file = v['file'];
            //     var filename = v['name'];
            //     var name = 'file-' + idx;
            //     formData.append(name, file, filename);
            // });
            // trail.num_files = files.length;
            // trail.input_name = 'events_trail_doc';
            //end append file code
            //trail.proposal = vm.proposal_id;

            formData.append('data', JSON.stringify(trail));
            //let trail = JSON.parse(JSON.stringify(vm.trail));
            vm.issuingPark = true;
            if(vm.trail_action=="add" && vm.trail_id==null)
            {
                vm.$http.post(api_endpoints.proposal_events_trails,formData,{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.issuingPark = false;
                        vm.trail={};
                        vm.close();
                        swal(
                             'Created',
                             'New trail record has been created.',
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
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.proposal_events_trails,vm.trail_id+'/edit_trail'),formData,{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.issuingPark = false;
                        vm.trail={};
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
            $(vm.$refs.events_trail).select2({
                "theme": "bootstrap",
                allowClear: true,
                placeholder:"Select Park"
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                vm.events_trail_id = selected.val();
                //vm.fetchSections();
            }).
            on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                vm.events_trail_id = selected.val();
                //vm.fetchSections();
            });
            $(vm.$refs.events_section).select2({
                "theme": "bootstrap",
                allowClear: true,
                placeholder:"Select section"
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                vm.section_id = selected.val();
                //vm.fetchAllowedActivities();
            }).
            on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                vm.section_id = selected.val();
                //vm.fetchAllowedActivities();
            });
            //Initialise select2 for Activity types
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
        vm.fetchAllTrails();
        vm.form = document.forms.parkForm;
        vm.addFormValidations();
        this.$nextTick(()=>{
            vm.eventListeners();
        });
        //vm.park.events_trail_documents = vm.$refs.filefield.uploaded_documents;
   }
}
</script>

<style lang="css">
</style>
