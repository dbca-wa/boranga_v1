<template id="park_table">
    <div class="row">
        <div class="col-sm-12"> 
            <div class="row" >
                <div class="col-md-3" v-if="canEditActivities">
                            <!-- <button style="margin-top:25px;" class="btn btn-primary pull-right">New Application</button> -->
                            <input type="button" style="margin-top:25px;" @click.prevent="newPark" class="btn btn-primary" value="Add" />
                </div>
            </div>

            <div class="row">
                <div class="col-lg-12" style="margin-top:25px;">
                    <datatable ref="park_datatable" :id="datatable_id" :dtOptions="park_options" :dtHeaders="park_headers"/>
                </div>
            </div>
        </div>
        <editPark ref="edit_park" :park_id="park_id" @refreshFromResponse="refreshFromResponse" :district_proposal="district_proposal" :is_external="is_external"></editPark>
    </div>
</template> 
<script>
import datatable from '@/utils/vue/datatable.vue'
import editPark from './edit_park.vue'
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'ParkTableDash',
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
    },
    data() {
        let vm = this;
        return {
            new_park:{
                park: null,
                feature_of_interest:'',
                from_date:null,
                to_date:null,
                 proposal: vm.proposal.id
            },
            pBody: 'pBody' + vm._uid,
            datatable_id: 'park-datatable-'+vm._uid,
            // Filters for Parks
            park_headers:["Park or Reserve","Feature or site of Interest","From","To","Itinerary/ Maps","Action"],
            park_options:{
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                responsive: true,
                //serverSide: true,
                //lengthMenu: [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
                ajax: {
                    "url": vm.url,
                    "dataSrc": '',

                    // adding extra GET params for Custom filtering
                    // "data": function ( d ) {
                    //     //d.regions = vm.filterParkRegion.join();
                    //     d.date_from = vm.filterComplianceDueFrom != '' && vm.filterComplianceDueFrom != null ? moment(vm.filterComplianceDueFrom, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                    //     d.date_to = vm.filterComplianceDueTo != '' && vm.filterComplianceDueTo != null ? moment(vm.filterComplianceDueTo, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                    // }

                },
                dom: 'lBfrtip',
                buttons:[
                'excel', 'csv', ],
                columns: [
                    // {
                    //     data: "id",
                    //     mRender:function (data,type,full) {
                    //         //return `C${data}`;
                    //         return full.id;
                    //     },
                    //     //name: "id, lodgement_number",
                    // },
                    {
                        data: "park",
                        mRender:function (data,type,full) {
                            //return `C${data}`;
                            return data.name;
                        },
                        //name: "park__region__name" // will be use like: Approval.objects.filter(park__region__name='Kimberley')
                    },
                    {
                        data: "feature_of_interest",

                        //name: "park__activity",
                    },
                    {
                        data: "from_date",
                        //name: "park__title",
                    },
                    {
                        data: "to_date",
                        // mRender:function (data,type,full) {
                        //     return `A${data}`;
                        // },
                        // name: "approval__lodgement_number"
                    },
                    {
                        data: 'filming_park_documents',
                        mRender:function (data,type,full) {
                            let links = '';
                            _.forEach(data, function (item) {
                                links += `<a href='${item._file}' target='_blank' style='padding-left: 52px;'>${item.name}</a><br/>`;
                            });
                            return links;
                        },
                    },
                    {
                        data: '',
                        mRender:function (data,type,full) {
                            let links = '';
                            if(vm.is_external){
                                if(!vm.proposal.readonly && full.park.visible_to_external){
                                links +=  `<a href='#${full.id}' data-edit-park='${full.id}'>Edit Park</a><br/>`;
                                links +=  `<a href='#${full.id}' data-discard-park='${full.id}'>Discard</a><br/>`;
                                }
                            }
                            if(!vm.is_external){
                                if(full.can_assessor_edit){
                                    links +=  `<a href='#${full.id}' data-edit-park='${full.id}'>Edit Park</a><br/>`;
                                    links +=  `<a href='#${full.id}' data-discard-park='${full.id}'>Discard</a><br/>`;
                                }
                            }
                        //     if (!vm.is_external){
                        //         if (full.can_user_view) {
                        //             links +=  `<a href='/internal/compliance/${full.id}'>Process</a><br/>`;
                                    
                        //         }
                        //         else {
                        //             links +=  `<a href='/internal/compliance/${full.id}'>View</a><br/>`;
                        //         }
                        //     }
                        //     else{
                        //         if (full.can_user_view) {
                        //             links +=  `<a href='/external/compliance/${full.id}'>View</a><br/>`;
                                    
                        //         }
                        //         else {
                        //             links +=  `<a href='/external/compliance/${full.id}'>Submit</a><br/>`;
                        //         }
                        //     }
                            return links;
                        },
                        // name: ''  
                    },
                    // {data: "reference", visible: false},
                    // {data: "customer_status", visible: false},
                    // {data: "can_user_view", visible: false},

                ],
                processing: true,
                /*
                initComplete: function () {
                    // Grab Regions from the data in the table
                    var regionColumn = vm.$refs.park_datatable.vmDataTable.columns(1);
                    regionColumn.data().unique().sort().each( function ( d, j ) {
                        let regionTitles = [];
                        $.each(d,(index,a) => {
                            // Split region string to array
                            if (a != null){
                                $.each(a.split(','),(i,r) => {
                                    r != null && regionTitles.indexOf(r) < 0 ? regionTitles.push(r): '';
                                });
                            }
                        })
                        vm.park_regions = regionTitles;
                    });
                    // Grab Activity from the data in the table
                    var titleColumn = vm.$refs.park_datatable.vmDataTable.columns(2);
                    titleColumn.data().unique().sort().each( function ( d, j ) {
                        let activityTitles = [];
                        $.each(d,(index,a) => {
                            a != null && activityTitles.indexOf(a) < 0 ? activityTitles.push(a): '';
                        })
                        vm.park_activityTitles = activityTitles;
                    });

                    // Grab Status from the data in the table
                    var statusColumn = vm.$refs.park_datatable.vmDataTable.columns(6);
                    statusColumn.data().unique().sort().each( function ( d, j ) {
                        let statusTitles = [];
                        $.each(d,(index,a) => {
                            a != null && statusTitles.indexOf(a) < 0 ? statusTitles.push(a): '';
                        })
                        vm.status = statusTitles;
                    });
                }
                */
            }
        }
    },
    components:{
        datatable,
        editPark
    },
    watch:{
    },
    computed: {
       /* status: function(){
            return this.is_external ? this.external_status : this.internal_status;
            //return [];
        }, */
        // is_external: function(){
        //     return this.level == 'external';
        // },
    },
    methods:{
        fetchFilterLists: function(){
            let vm = this;

            // vm.$http.get(api_endpoints.filter_list_compliances).then((response) => {
            //     vm.park_regions = response.body.regions;
            //     vm.park_activityTitles = response.body.activities;
            //     vm.status = vm.level == 'external' ? vm.external_status: vm.internal_status;
            // },(error) => {
            //     console.log(error);
            // })
            //console.log(vm.regions);
        },
        newPark: function(){
            let vm=this;
            this.$refs.edit_park.park_id = null;
            //this.$refs.edit_park.fetchPark(id);
            var new_park_another={
                park: null,
                feature_of_interest:'',
                from_date:null,
                to_date:null,
                proposal: vm.proposal.id
            }
            //this.$refs.edit_park.park=this.new_park;
            this.$refs.edit_park.park=new_park_another;
            this.$refs.edit_park.park_action='add'
            this.$refs.edit_park.isModalOpen = true;
        },
        editPark: function(id){
            this.$refs.edit_park.park_id = id;
            this.$refs.edit_park.fetchPark(id);
            this.$refs.edit_park.isModalOpen = true;
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
                vm.$http.delete(api_endpoints.discard_filming_park(park_id))
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
        // if(vm.is_external){
        //     var column = vm.$refs.park_datatable.vmDataTable.columns(8); //Hide 'Assigned To column for external'
        //     column.visible(false);
        // }
        
    }
}
</script>
<style scoped>
</style>
