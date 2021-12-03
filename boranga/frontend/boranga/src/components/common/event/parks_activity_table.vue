<template id="event_parks_activity_table">
    <div class="">
        <div class="col-sm-12"> 
            <div class="row" >
                <div class="col-md-3" v-if="canEditActivities">
                            <!-- <button style="margin-top:25px;" class="btn btn-primary pull-right">New Application</button> -->
                            <input type="button" style="margin-top:25px;" @click.prevent="newPark" class="btn btn-primary" value="Add" />
                </div>
            </div>
            <div class="row">&nbsp;</div>
            <div class="row" >
                <div class="" >
                            <label class="col-sm-12"  for="Name">Please attach a detailed itinerary and map of the event route (including a GPX or KML file format). Please include information on the proposed routes, parking and staging locations, spectator points and camping sites, and any mustering, changeover, aid station or transition points.</label>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-12">
                    <FileField :proposal_id="proposal.id" isRepeatable="true" name="event_park_maps" :id="'proposal'+proposal.id" :readonly="proposal.readonly" ref="event_park_maps"></FileField>    
                </div>
            </div>

            <div class="row">
                <div class="col-lg-12" style="margin-top:25px;">
                    <datatable ref="park_datatable" :id="datatable_id" :dtOptions="park_options" :dtHeaders="park_headers"/>
                </div>
            </div>
        </div>
        <editPark ref="edit_park" :park_id="park_id" @refreshFromResponse="refreshFromResponse" :is_internal="is_internal" :is_external="is_external"></editPark>
        <!-- v-bind:key="editParkBindId" -->
    </div>
</template> 
<script>
import datatable from '@/utils/vue/datatable.vue'
import editPark from './edit_park_activity.vue'
import FileField from '@/components/forms/filefield.vue'
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'EventParkTableDash',
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
            datatable_id: 'park-datatable-'+vm._uid,
            uuid: 0,
            // Filters for Parks
            //park_headers:["Park or Reserve","Activities","Itinerary/ Maps","Action"],
            park_headers:["Park or Reserve","Activities (application)","Activities (assessor)","Action"],
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
                        data: "park",
                        mRender:function (data,type,full) {
                            //return `C${data}`;
                            return data.name;
                        },
                        
                    },
                    {
                        //data: "activities_names",
                        data: "event_activities",

                        //name: "park__activity",
                    },
                    {
                        data: "activities_assessor_names",

                    },
                    // {
                    //     data: 'events_park_documents',
                    //     mRender:function (data,type,full) {
                    //         let links = '';
                    //         _.forEach(data, function (item) {
                    //             links += `<a href='${item._file}' target='_blank' style='padding-left: 52px;'>${item.name}</a><br/>`;
                    //         });
                    //         return links;
                    //     },
                    // },
                    {
                        data: '',
                        mRender:function (data,type,full) {
                            let links = '';
                        //     if(!vm.proposal.readonly){
                        //     links +=  `<a href='#${full.id}' data-edit-park='${full.id}'>Edit Park</a><br/>`;
                        //     links +=  `<a href='#${full.id}' data-discard-park='${full.id}'>Discard</a><br/>`;
                        // }
                        if(vm.canEditActivities){
                            if(vm.is_external){
                                if(full.park.visible_to_external){
                                    links +=  `<a href='#${full.id}' data-edit-park='${full.id}'>Edit</a><br/>`;
                                    links +=  `<a href='#${full.id}' data-discard-park='${full.id}'>Discard</a><br/>`;
                                }
                            }
                            else{

                            links +=  `<a href='#${full.id}' data-edit-park='${full.id}'>Edit</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-park='${full.id}'>Discard</a><br/>`;
                            }
                        
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
        editPark,
        FileField,
    },
    watch:{
    },
    computed: {
        // is_external: function(){
        //     return this.level == 'external';
        // },
        editParkBindId: function(){
            let edit_park_bind_id='';
            edit_park_bind_id='editPark' + parseInt(this.uuid);
            return edit_park_bind_id;
        },
    },
    methods:{
        fetchFilterLists: function(){
            let vm = this;
        },
        newPark: function(){
            let vm=this;
            this.uuid +=1;

            this.$nextTick(() =>{
                this.$refs.edit_park.park_id = null;
            //this.$refs.edit_park.fetchPark(id);
                var new_park_another={
                    park: null,
                    activities:[],
                    proposal: vm.proposal.id
                }
                //this.$refs.edit_park.park=this.new_park;
                this.$refs.edit_park.park=new_park_another;
                this.$refs.edit_park.park_action='add'

                this.$refs.edit_park.isModalOpen = true;
            });
            // this.$refs.edit_park.park_id = null;
            // //this.$refs.edit_park.fetchPark(id);
            // var new_park_another={
            //     park: null,
            //     activities:[],
            //     proposal: vm.proposal.id
            // }
            // //this.$refs.edit_park.park=this.new_park;
            // this.$refs.edit_park.park=new_park_another;
            // this.$refs.edit_park.park_action='add'

            // this.$refs.edit_park.isModalOpen = true;
        },
        editPark: function(id){
            this.uuid +=1;
            this.$nextTick(() =>{
                this.$refs.edit_park.park_id = id;
                // this.$refs.edit_park.events_park_id = id;
                // $(this.$refs.events_park).val(id).trigger('change');
                this.$refs.edit_park.fetchPark(id);
                this.$refs.edit_park.isModalOpen = true;
            });
        },
        discardPark:function (park_id) {
            let vm = this;
            swal({
                title: "Discard Park",
                text: "Are you sure you want to discard this park?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Park',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_event_park(park_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Your park has been discarded',
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
                vm.editPark(id);
            });
            // External Discard listener
            vm.$refs.park_datatable.vmDataTable.on('click', 'a[data-discard-park]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-park');
                vm.discardPark(id);
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
            var column = vm.$refs.park_datatable.vmDataTable.columns(2); 
            column.visible(false);
        }
        
    }
}
</script>
<style scoped>
</style>
