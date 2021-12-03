<template id="event_trails_activity_table">
    <div class="">
        <div class="col-sm-12"> 
            <div class="row" >
                <div class="col-md-3" v-if="canEditActivities">
                            <!-- <button style="margin-top:25px;" class="btn btn-primary pull-right">New Application</button> -->
                            <input type="button" style="margin-top:25px;" @click.prevent="newTrail" class="btn btn-primary" value="Add" />
                </div>
            </div>
            <div class="row">&nbsp;</div>
            <!-- <div class="row" >
                <div class="" >
                            <label class="col-sm-12"  for="Name">Please attach a detailed itinerary and map of the event route (including a GPX or KML file format). Please include information on the proposed routes, spectator points and camping sites, and any mustering, changeover, aid station or transition points.</label>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-12">
                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="event_park_maps" :id="'proposal'+proposal.id" :readonly="proposal.readonly"></FileField>    
                </div>
            </div> -->

            <div class="row">
                <div class="col-lg-12" style="margin-top:25px;">
                    <datatable ref="park_datatable" :id="datatable_id" :dtOptions="park_options" :dtHeaders="park_headers"/>
                </div>
            </div>
        </div>
        <editTrail ref="edit_trail" :trail_id="trail_id" @refreshFromResponse="refreshFromResponse" :is_internal="is_internal"></editTrail>
        <!-- v-bind:key="editParkBindId" -->
    </div>
</template> 
<script>
import datatable from '@/utils/vue/datatable.vue'
//import editPark from './edit_trail_activity.vue'
import editTrail from './edit_trail_activity.vue'
import FileField from '@/components/forms/filefield.vue'
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'EventTrailTableDash',
    props: {
        // level:{
        //     type: String,
        //     required: true,
        //     validator:function(val) {
        //         let options = ['internal','referral','external'];
        //         return options.indexOf(val) != -1 ? true: false;
        //     }
        // },
        proposal:{
                type: Object,
                required:true
        },
        url:{
            type: String,
            required: true
        },
        canEditActivities:{
              type: Boolean,
              default: true
        },
        is_internal:{
              type: Boolean,
              default: false
        },
        is_external:{
              type: Boolean,
              default: false
        },

    },
    data() {
        let vm = this;
        return {
            new_park:{
                park: null,
                activities:[],
                proposal: vm.proposal.id
            },
            pBody: 'pBody' + vm._uid,
            datatable_id: 'trail-datatable-'+vm._uid,
            uuid: 0,
            // Filters for Parks
            //park_headers:["Park or Reserve","Activities","Itinerary/ Maps","Action"],
            park_headers:["Trail","Section","Activities (application)","Activities (assessor)","Action"],
            park_options:{
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                responsive: true,
                ajax: {
                    "url": vm.url,
                    "dataSrc": '',

                },
                dom: 'lBfrtip',
                buttons:[
                'excel', 'csv', ],
                columns: [
                    
                    {
                        data: "trail",
                        mRender:function (data,type,full) {
                            //return `C${data}`;
                            return data.name;
                        },
                        
                    },
                    {
                        data: "section",

                        mRender:function (data,type,full) {
                            if(data){
                                return data.name;
                            }
                            else{
                                return '';
                            }
                        },
                    },
                    {
                        data: "event_trail_activities",

                    },
                    {
                        data: "activities_assessor_names",

                    },
                    {
                        data: '',
                        mRender:function (data,type,full) {
                            let links = '';
                        //     if(!vm.proposal.readonly){
                        //     links +=  `<a href='#${full.id}' data-edit-park='${full.id}'>Edit Park</a><br/>`;
                        //     links +=  `<a href='#${full.id}' data-discard-trail='${full.id}'>Discard</a><br/>`;
                        // }
                        if(vm.canEditActivities){
                            links +=  `<a href='#${full.id}' data-edit-park='${full.id}'>Edit</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-trail='${full.id}'>Discard</a><br/>`;
                        }
                            return links;
                        },
                    },

                ],
                processing: true,
            }
        }
    },
    components:{
        datatable,
        editTrail,
        FileField,
    },
    watch:{
    },
    computed: {
        // is_external: function(){
        //     return this.level == 'external';
        // },
        editParkBindId: function(){
            let edit_trail_bind_id='';
            edit_trail_bind_id='editPark' + parseInt(this.uuid);
            return edit_trail_bind_id;
        },
    },
    methods:{
        fetchFilterLists: function(){
            let vm = this;
        },
        newTrail: function(){
            let vm=this;
            this.uuid +=1;

            this.$nextTick(() =>{
                this.$refs.edit_trail.trail_id = null;
            //this.$refs.edit_trail.fetchtrail(id);
                var new_trail_another={
                    trail: null,
                    section: null,
                    event_trail_activities:'',
                    proposal: vm.proposal.id
                }
                //this.$refs.edit_trail.trail=this.new_trail;
                this.$refs.edit_trail.trail=new_trail_another;
                this.$refs.edit_trail.trail_action='add'

                this.$refs.edit_trail.isModalOpen = true;
            });
        },
        editTrail: function(id){
            this.uuid +=1;
            this.$nextTick(() =>{
                this.$refs.edit_trail.trail_id = id;
                // this.$refs.edit_trail.events_park_id = id;
                // $(this.$refs.events_park).val(id).trigger('change');
                this.$refs.edit_trail.fetchTrail(id);
                this.$refs.edit_trail.isModalOpen = true;
            });
        },
        discardTrail:function (trail_id) {
            let vm = this;
            swal({
                title: "Discard Trail",
                text: "Are you sure you want to discard this trail?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Trail',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_event_trail(trail_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Your trail has been discarded',
                        'success'
                    )
                    vm.$refs.park_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            vm.$refs.park_datatable.vmDataTable.on('click', 'a[data-edit-park]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-edit-park');
                vm.editTrail(id);
            });
            // External Discard listener
            vm.$refs.park_datatable.vmDataTable.on('click', 'a[data-discard-trail]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-trail');
                vm.discardTrail(id);
            });
        },
        refreshFromResponse: function(){
            this.$refs.park_datatable.vmDataTable.ajax.reload();
        },
        initialiseSearch:function(){
            
        }, 
    },
    mounted: function(){
        let vm = this;
        vm.fetchFilterLists();
        this.$nextTick(() => {
            vm.addEventListeners();
            vm.initialiseSearch();
        });
        if(vm.is_external){
            var column = vm.$refs.park_datatable.vmDataTable.columns(3); //Hide 'Assigned To column for external'
            column.visible(false);
        }
        
    }
}
</script>
<style scoped>
</style>
