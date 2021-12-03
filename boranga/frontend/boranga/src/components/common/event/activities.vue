<template lang="html">
<div class="row" id="activityInfo">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Event Details <small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#activityInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">                        
                        <div class="">
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-right"  for="Name">Event name</label>
                                </div>
                                <div class="col-sm-9">
                                    <!-- <input type="text" class="form-control" v-model="proposal.activities_event.event_name" name="event_name" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal"> -->
                                    <input type="text" class="form-control" name="event_name" :disabled="!canEditPeriod || proposal.pending_amendment_request || proposal.is_amendment_proposal" v-model="proposal.event_activity.event_name">
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>

                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-right"  for="Name">Period of proposed event</label>
                                </div>
                                <div class="col-sm-4">
                                    <div class="input-group date" ref="event_activity_commencement_date" style="width: 70%;">
                                        <input type="text" class="form-control" v-model="proposal.event_activity.commencement_date" name="event_activity_commencement_date" placeholder="Commencement date" :disabled="!canEditPeriod || proposal.pending_amendment_request || proposal.is_amendment_proposal">
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="input-group date" ref="event_activity_completion_date" style="width: 70%;">
                                        <input type="text" class="form-control" v-model="proposal.event_activity.completion_date" name="event_activity_completion_date" placeholder="Completion date" :disabled="!canEditPeriod || proposal.pending_amendment_request || proposal.is_amendment_proposal">
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row" v-if="is_internal || is_referral">
                                <div class="col-sm-3">
                                    <label class="control-label pull-right"  for="Name">Event date</label>
                                </div>
                                <div class="col-sm-9">
                                    <!-- <input type="text" class="form-control" v-model="proposal.activities_event.event_name" name="event_name" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal"> -->
                                    <input type="text" class="form-control" name="event_date" :disabled="!canEditPeriod || proposal.pending_amendment_request || proposal.is_amendment_proposal" v-model="proposal.event_activity.event_date">
                                </div>
                            </div>
                        </div> 
                    </div>

                    <div class="form-horizontal col-sm-12 borderDecoration">                        
                        <div class="">
                            <div class="row">
                                <label class="col-sm-12"  for="Name">List the parks (terrestrial and/or marine) where this event is proposed to occur and add the proposed activities to be undertaken in each park.</label>
                                <ParksActivityTable :url="parks_url" :proposal="proposal"  ref="parks_table":canEditActivities="canEditActivities" :is_internal="is_internal" :is_external="is_external"></ParksActivityTable>
                            </div>
                            <div class="row">&nbsp;</div>
                        </div> 
                    </div>

                    <!-- <div class="form-horizontal col-sm-12 borderDecoration">                        
                        <div class="">
                            <div class="">
                                <AbseilingClimbingTable :url="abseiling_climbing_url" :proposal="proposal"  ref="abseiling_climbing_table"></AbseilingClimbingTable>
                            </div>
                            <div class="row">&nbsp;</div>
                        </div> 
                    </div> -->
                    <div class="form-horizontal col-sm-12 borderDecoration">                        
                        <div class="">
                            <div class="row">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Is any part of your proposed event located within Public Drinking Water Source Areas (PDSWA)?</label>                                   
                                </div>
                              <div class="col-sm-6">
                                  <ul class="list-inline"  >
                                      <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_activity.pdswa_location" :value="true" data-parsley-required :disabled="proposal.readonly" name="pdswa_location"/>
                                            Yes
                                      </li>
                                      <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.event_activity.pdswa_location" :value="false" data-parsley-required :disabled="proposal.readonly" name="pdswa_location"/>
                                            No
                                      </li>
                                  </ul>      
                                </div>
                            </div>
                            <div class="row" v-if="proposal.event_activity.pdswa_location">
                                <div class="col-sm-6">
                                    <label v-if="dwer_application_form" class="control-label pull-left"  for="Name">Please complete and attach the Department of Water and Environmental Regulation application form accessible  <a :href="dwer_application_form" target="_blank">here</a>.</label>
                                    <label v-else class="control-label pull-left"  for="Name">Please complete and attach the Department of Water and Environmental Regulation application form accessible here.</label>                               
                                </div>
                                <div class="col-sm-6">
                                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="event_activity_pdswa_location" :id="'proposal'+proposal.id" :readonly="proposal.readonly" ref="event_activity_pdswa_file"></FileField>
                                </div>                                
                            </div>
                            <div class="row">&nbsp;</div> 
                        </div> 
                    </div>

                </div>
            </div>                
        </div>
    <div class="panel panel-default">
        <div class="panel-heading">
          <h3 class="panel-title">Activities and Location <small> (Trails)</small>
            <a class="panelClicker" :href="'#'+tBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="tBody">
              <span class="glyphicon glyphicon-chevron-up pull-right "></span>
            </a>
          </h3>
        </div>

        <div class="panel-body collapse in" :id="tBody">
          <div>

            <div class="">
                <div class="row">
                    <label v-if="trail_section_map" class="col-sm-12"  for="Name">List the the track and trail sections where this event is proposed to occur and add the proposed activties to be undertaken. A map of the sections can be viewed <a :href="trail_section_map" target="_blank">here</a>.</label>
                    <label v-else="trail_section_map" class="col-sm-12"  for="Name">List the the track and trail sections where this event is proposed to occur and add the proposed activties to be undertaken. A map of the sections can be viewed here.</label>
                        <TrailsActivityTable :url="trails_url" :proposal="proposal"  ref="trails_table":canEditActivities="canEditActivities" :is_internal="is_internal" :is_external="is_external"></TrailsActivityTable>
                </div>
                <div class="row">&nbsp;</div>
            </div> 

            <!-- <div class="borderDecoration col-sm-12">
                <form>
                    <div class="col-sm-12" >
                        <div>
                            <label class="control-label">Select the required activities for trails</label>
                            <TreeSelect :proposal="proposal" :value.sync="trail_activities" :options="trail_activity_options" :default_expand_level="1" :disabled="!canEditActivities"></TreeSelect>
                        </div>
                    </div>
                </form>
            </div>

            <div class="borderDecoration col-sm-12">
                <form>
                    <div class="col-sm-12" >
                        <div>
                            <label class="control-label">Select the long distance trails</label>
                            <TreeSelect :proposal="proposal" :value.sync="selected_trail_ids" :options="trail_options" :default_expand_level="1" open_direction="top" allow_edit="true" :disabled="!canEditActivities"></TreeSelect>
                        </div>
                    </div>
                </form>
            </div> -->
            
            <!-- <div>Trail_actvities: {{trail_activities}}</div><br>
            <div>Selected_Trail: {{selected_trail_ids}}</div><br>
            <div>Selected_Trailss_Activities: {{selected_trails_activities}}</div> -->
            
          </div>
        </div>
    </div>
      <!-- <div>
              <editTrailActivities ref="edit_sections" :proposal="proposal" :canEditActivities="canEditActivities" @refreshTrailFromResponse="refreshTrailFromResponse"></editTrailActivities>
      </div> -->
    </div>

</div>
</template>

<script>
import ParksActivityTable from './parks_activity_table.vue'
import TrailsActivityTable from './trails_activity_table.vue'
import AbseilingClimbingTable from './abseiling_climbing_table.vue'
import editTrailActivities from '@/components/common/tclass/edit_trail_activities.vue'
//import editTrailActivities from './edit_trail_activities.vue'
import TreeSelect from '@/components/forms/treeview.vue'
import FileField from '@/components/forms/filefield.vue'
import {
  api_endpoints,
  helpers
}from '@/utils/hooks'
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
            hasDistrictAssessorMode:{
                type:Boolean,
                default: false
            },
            is_external:{
              type: Boolean,
              default: false
            },
            canEditPeriod:{
              type: Boolean,
              default: false
            },
            hasAssessorMode:{
                type:Boolean,
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
        },
        data:function () {
            let vm = this;
            return{
                lBody: 'lBody'+vm._uid,
                tBody: 'tBody'+vm._uid,
                values:null,
                parks_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.proposal_id+'/events_parks'),
                trails_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.proposal_id+'/events_trails'),
                abseiling_climbing_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.proposal_id+'/abseiling_climbing_activities'),
                trail_options: [],
                trail_activity_options: [],
                trails:null,
                land_activity_options: [],
                selected_trail_ids:[],
                trail_activities:[],
                selected_trails_activities:[],
                global_settings:[],
                datepickerOptions:{
                    format: 'DD/MM/YYYY',
                    showClear:true,
                    useCurrent:false,
                    keepInvalid:true,
                    allowInputToggle:true,
                },
            }
        },
        components:{
            ParksActivityTable,
            TrailsActivityTable,
            AbseilingClimbingTable,
            TreeSelect,
            editTrailActivities,
            FileField,
        },
        computed:{
            trail_section_map: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='trail_section_map'){
                            return vm.global_settings[i].value;
                        }
                    }
                }
                return '';
            },
            dwer_application_form: function(){
                let vm=this;
                if(vm.global_settings){
                    for(var i=0; i<vm.global_settings.length; i++){
                        if(vm.global_settings[i].key=='dwer_application_form'){
                            return vm.global_settings[i].value;
                        }
                    }
                }
                return '';
            },
        },
        watch:{
            selected_trail_ids: function(){
            let vm=this;
            //if (vm.proposal){
            //  vm.proposal.trails=vm.selected_trails;
            //}

            vm.selected_trails = []
            for (var i = 0; i < vm.selected_trail_ids.length; i++) {
                var data = vm.get_selected_trail_data(vm.selected_trail_ids[i] )
                if (data !== null) {
                    vm.selected_trails.push( data )
                }
            }

            try {
                var removed_trail_id=$(vm.selected_trail_ids_before).not(vm.selected_trail_ids).get();
            } catch (error) {
                console.log('removed_trail: ' + error)
            }

            try {
                var added_trail_id=$(vm.selected_trail_ids).not(vm.selected_trail_ids_before).get();
            } catch (error) {
                console.log('added_trail: ' + error)
            }
            vm.selected_trail_ids_before=vm.selected_trail_ids;

            var current_activities=vm.trail_activities

            if(vm.selected_trails_activities.length==0){
              for (var i = 0; i < vm.selected_trails.length; i++) {
                 var data=null;
                 var section_activities=[];

                 for (var j=0; j<vm.selected_trails[i].sections.length; j++){
                  var section_data={
                    'section': vm.selected_trails[i].sections[j],
                    'activities': current_activities
                  }
                  section_activities.push(section_data)
                 }
                 data={
                  'trail': vm.selected_trails[i].trail,
                  'activities': section_activities 
                 }
                 vm.selected_trails_activities.push(data);
              }
            }
            else{
              if(added_trail_id.length!=0){
                for(var i=0; i<added_trail_id.length; i++) {
                  var found=false
                  for (var j=0; j<vm.selected_trails_activities.length; j++){
                        //console.log(added_trail[i])
                        if(vm.selected_trails_activities[j].trail==added_trail_id[i]){
                          found = true;
                        }
                  }
                  if(found==false) {
                    //original data object
                    var section_activities=[];
                    var trail_data = vm.get_selected_trail_data(added_trail_id[i] )
                    if (trail_data !== null) {
                        for(var k=0; k<trail_data.sections.length; k++){
                          var section_data={
                          'section': trail_data.sections[k],
                          'activities': current_activities
                          }
                          section_activities.push(section_data)
                        }
                        data={
                          'trail': added_trail_id[i],
                          'activities': section_activities
                        }
                    }
                    vm.selected_trails_activities.push(data);
                  }
                }
              }
              if(removed_trail_id.length!=0){
                for(var i=0; i<removed_trail_id.length; i++)
                { 
                  for (var j=0; j<vm.selected_trails_activities.length; j++){
                    if(vm.selected_trails_activities[j].trail==removed_trail_id[i]){
                      vm.selected_trails_activities.splice(j,1)}
                  }
                }
              }
            }
            if (vm.proposal){
              vm.proposal.trails=vm.selected_trails;
              vm.proposal.selected_trails_activities=vm.selected_trails_activities;
            }
          },
          selected_trails_activities: function(){
            let vm=this;

            if (vm.proposal){
              vm.proposal.selected_trails_activities=vm.selected_trails_activities;
            }
            },
          trail_activities: function(){
          let vm=this;
          var removed=$(vm.trail_activities_before).not(vm.trail_activities).get();
          var added=$(vm.trail_activities).not(vm.trail_activities_before).get();
          vm.trail_activities_before=vm.trail_activities;
          if(vm.selected_trails_activities.length==0){
            for (var i = 0; i < vm.selected_trail_ids.length; i++) {
                 var data=null;
                 data={
                  'trail': vm.selected_trail_ids[i],
                  'activities': vm.trail_activities
                 }
                 vm.selected_trails_activities.push(data);
               }
          }
          else{
            for (var i=0; i<vm.selected_trails_activities.length; i++)
            {
              if(added.length!=0){
                for(var j=0; j<added.length; j++)
                {
                  // if(vm.selected_trails_activities[i].activities.indexOf(added[j])<0){
                  //   vm.selected_trails_activities[i].activities.push(added[j]);
                  // }
                  for(var k=0; k<vm.selected_trails_activities[i].activities.length; k++){
                    if(vm.selected_trails_activities[i].activities[k].activities.indexOf(added[j])<0){
                    vm.selected_trails_activities[i].activities[k].activities.push(added[j]);
                    }
                  }
                }
              }
              if(removed.length!=0){
                for(var j=0; j<removed.length; j++)
                {
                  for(var k=0; k<vm.selected_trails_activities[i].activities.length; k++){
                    var index=vm.selected_trails_activities[i].activities[k].activities.indexOf(removed[j]);
                    if(index!=-1){
                      vm.selected_trails_activities[i].activities[k].activities.splice(index,1)
                    }
                  }

                }
              }
            }
          }
        },  
        },
        methods:{
            get_selected_trail_data:function(trail_id){
            let vm = this;
            for (var i=0; i<vm.trails.length; i++) {
              if (vm.trails[i].id == trail_id) {
                //console.log(vm.trails[i].section_ids)
                return {'trail': trail_id, 'sections': vm.trails[i].section_ids}
              }
            }
            return null;
          },
          get_selected_trail_ids:function(node){
            let vm = this;

            var ids = []
            for (var i=0; i<vm.selected_trails.length; i++) {
                ids.push( vm.selected_trails[i].trail )
            }
            return ids.filter(function(item, pos) { return ids.indexOf(item) == pos;  }) // returns unique array ids
          },
          edit_sections: function(node){
            let vm=this;
            var trail = node.raw;
            //trail['id']=node.id

            console.log('Trail 0: ' + JSON.stringify(trail))
            //inserting a temporary variables checked and new_activities to store and display selected activities for each section.
            for(var l=0; l<trail.sections.length; l++){
              trail.sections[l].checked=false;
              trail.sections[l].activities=[];
              trail.sections[l].new_activities=[];
            }

            for (var i=0; i<vm.selected_trails_activities.length; i++){
              if(vm.selected_trails_activities[i].trail==trail.id){
                for(var j=0; j<vm.selected_trails_activities[i].activities.length; j++){
                  for(var k=0; k<trail.sections.length; k++){
                    if (trail.sections[k].id==vm.selected_trails_activities[i].activities[j].section){
                      trail.sections[k].checked=true;
                      trail.sections[k].new_activities=vm.selected_trails_activities[i].activities[j].activities
                    }
                  }
                } 
              }
            }
            console.log('Trail: ' + JSON.stringify(trail))
            this.$refs.edit_sections.trail=trail;
            this. $refs.edit_sections.isModalOpen = true;
          },
          refreshTrailFromResponse: function(trail_id, new_activities){
              let vm=this;
              for (var j=0; j<vm.selected_trails_activities.length; j++){
              if(vm.selected_trails_activities[j].trail==trail_id){ 
                vm.selected_trails_activities[j].activities= new_activities;
              }
            }
          },
          find_repeated: function(array){
            var common=new Map();
            array.forEach(function(obj){
             var values=Object.values(obj)[0];
             values.forEach(function(val){
                 common.set(val,(common.get(val)||0)+1);
             });
            });
            var result=[];
            common.forEach(function(appearance,el){
               result.push(el);
            });
            return result;
          },
          eventListeners:function (){

                let vm=this;
                var date= new Date()
                var today= new Date(date.getFullYear(), date.getMonth(), date.getDate());

                $(vm.$refs.event_activity_commencement_date).datetimepicker(vm.datepickerOptions);
                //Set minimum date on datetimepicker so that nominated
                //start date cannot be selected prior to today
                $(vm.$refs.event_activity_commencement_date).data("DateTimePicker").minDate(today);
                $(vm.$refs.event_activity_commencement_date).on('dp.change', function(e){
                    if ($(vm.$refs.event_activity_commencement_date).data('DateTimePicker').date()) {
                        

                        vm.proposal.event_activity.commencement_date =  e.date.format('DD/MM/YYYY');
                    }
                    else if ($(vm.$refs.event_activity_commencement_date).data('date') === "") {
                        vm.proposal.event_activity.commencement_date = "";
                    }
                 });

                $(vm.$refs.event_activity_completion_date).datetimepicker(vm.datepickerOptions);
                //Set minimum date on datetimepicker so that nominated
                //start date cannot be selected prior to today
                $(vm.$refs.event_activity_completion_date).data("DateTimePicker").minDate(today);
                $(vm.$refs.event_activity_completion_date).on('dp.change', function(e){
                    if ($(vm.$refs.event_activity_completion_date).data('DateTimePicker').date()) {
                        

                        vm.proposal.event_activity.completion_date =  e.date.format('DD/MM/YYYY');
                    }
                    else if ($(vm.$refs.event_activity_completion_date).data('date') === "") {
                        vm.proposal.event_activity.completion_date = "";
                    }
                 });
          },
          fetchGlobalSettings: function(){
                let vm = this;
                vm.$http.get('/api/global_settings.json').then((response) => {
                    vm.global_settings = response.body;
                    
                },(error) => {
                    console.log(error);
                } );
            },

          store_trails: function(trails){
            let vm=this;
            var all_activities=[] //to store all activities for all sections so can find recurring ones to display selected_activities
            var trail_list=[]
            for (var i = 0; i < trails.length; i++) {
                var current_trail=trails[i].trail.id
                var current_activities=[]
                var current_sections=[]

                for (var j = 0; j < trails[i].sections.length; j++) {
                  var trail_activities=[];
                  for (var k = 0; k < trails[i].sections[j].trail_activities.length; k++) {
                    trail_activities.push(trails[i].sections[j].trail_activities[k].activity);
                  }
                  var data_section={
                    'section': trails[i].sections[j].section,
                    'activities': trail_activities
                  }
                  current_activities.push(data_section)
                  all_activities.push({'key': trail_activities})
                  //current_sections.push(trails[i].sections[j].section)
                }

                 var data={
                  'trail': current_trail,
                  'activities': current_activities 
                 }
                 vm.selected_trails_activities.push(data)
              }

            for (var i=0; i<trails.length; i++)
              {
                trail_list.push({'trail':trails[i].trail.id, 'sections':trails[i].trail.section_ids})
              }
            vm.selected_trails=trail_list
            //console.log(trail_list)
            //vm.trail_activities = vm.find_recurring(all_activities)
            vm.trail_activities = vm.find_repeated(all_activities)
          },
          fetchParkTreeview: function(){
            let vm = this;

            //console.log('treeview_url: ' + api_endpoints.tclass_container_land)
            vm.$http.get(api_endpoints.event_trail_container)
            .then((response) => {
                

                vm.land_activity_options = [
                    {
                        'id': 'All',
                        'name':'Select all',
                        'children': response.body['land_activity_types']
                    }
                ]
                vm.trail_activity_options = vm.land_activity_options
                vm.activities = response.body['land_activity_types'] // needed to pass to Vehicle component

                vm.trail_options = [
                    {
                        'id': 'All',
                        'name':'Select all',
                        'children': response.body['trails']
                    }
                ]
                vm.trails = response.body['trails']

            },(error) => {
                console.log(error);
            })
          },
        },
        mounted: function(){
            let vm=this;
            vm.fetchParkTreeview();
            vm.fetchGlobalSettings();
            this.$nextTick(()=>{
                vm.eventListeners();
            });
            vm.proposal.selected_trails_activities=[];
            vm.store_trails(vm.proposal.trails);
            vm.selected_trail_ids = vm.get_selected_trail_ids()
            vm.selected_trail_ids_before = vm.selected_trail_ids

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

