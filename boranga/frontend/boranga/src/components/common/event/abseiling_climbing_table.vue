<template id="abseiling_climbing_table">
    <div class="row">
        <div class="col-sm-12"> 
            <div class="row" >
                <div class="col-md-3" v-if="!proposal.readonly">
                            <!-- <button style="margin-top:25px;" class="btn btn-primary pull-right">New Application</button> -->
                            <input type="button" style="margin-top:25px;" @click.prevent="newRecord" class="btn btn-primary" value="Add" />
                </div>
            </div>

            <div class="row">
                <div class="col-lg-12" style="margin-top:25px;">
                    <datatable ref="abseiling_climbing_datatable" :id="datatable_id" :dtOptions="abseiling_climbing_options" :dtHeaders="abseiling_climbing_headers"/>
                </div>
            </div>
        </div>
        <editRecord ref="edit_abseiling_climbing" :abseiling_climbing_id="abseiling_climbing_id"  @refreshFromResponse="refreshFromResponse"></editRecord>
    </div>
</template>
<script>
import datatable from '@/utils/vue/datatable.vue'
import editRecord from './edit_abseiling_climbing.vue'
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'AbseilingClimbingTableDash',
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
    },
    data() {
        let vm = this;
        return {
            new_abseiling_climbing:{
                leader:'',
                rego_number:'',
                expiry_date:null,
                proposal: vm.proposal.id
            },
            pBody: 'pBody' + vm._uid,
            datatable_id: 'abseiling_climbing-datatable-'+vm._uid,
            // Filters for Vehicles
            external_status:[
                'Due',
                'Future',
                'Under Review',
                'Approved',
            ],
            internal_status:[
                'Due',
                'Future',
                'With Assessor',
                'Approved',
            ],
            // abseiling_climbing_headers:["Leader","NOLRS registration no.","Expiry Date","Action"],
            abseiling_climbing_headers:["Leader","Expiry Date","Action"],
            abseiling_climbing_options:{
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
                    //     //d.regions = vm.filterVehicleRegion.join();
                    //     d.date_from = vm.filterComplianceDueFrom != '' && vm.filterComplianceDueFrom != null ? moment(vm.filterComplianceDueFrom, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                    //     d.date_to = vm.filterComplianceDueTo != '' && vm.filterComplianceDueTo != null ? moment(vm.filterComplianceDueTo, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                    // }

                },
                dom: 'lBfrtip',
                buttons:[
                'excel', 'csv', ],
                columns: [
                    
                    {
                        data: "leader",
                        mRender:function (data,type,full) {
                            //return `C${data}`;
                            return data;
                        },
                        //name: "abseiling_climbing__region__name" // will be use like: Approval.objects.filter(abseiling_climbing__region__name='Kimberley')
                    },
                    // {
                    //     data: "rego_number",

                    //     //name: "abseiling_climbing__activity",
                    // },
                    {
                        data: "expiry_date",
                        //name: "abseiling_climbing__title",
                    },
                    {
                        data: '',
                        mRender:function (data,type,full) {
                            let links = '';
                            if(!vm.proposal.readonly){
                            links +=  `<a href='#${full.id}' data-edit-abseiling_climbing='${full.id}'>Edit</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-abseiling_climbing='${full.id}'>Discard</a><br/>`;
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
        editRecord
    },
    watch:{
    },
    computed: {
       /* status: function(){
            return this.is_external ? this.external_status : this.internal_status;
            //return [];
        }, */
        is_external: function(){
            return this.level == 'external';
        },
    },
    methods:{
        fetchFilterLists: function(){
            let vm = this;

            
        },
        newRecord: function(){
            let vm=this;
            this.$refs.edit_abseiling_climbing.abseiling_climbing_id = null;
            //this.$refs.edit_abseiling_climbing.fetchVehicle(id);
            var new_abseiling_climbing_another={
                leader:'',
                expiry_date:null,
                rego_number:'',
                proposal: vm.proposal.id,
                event_activities: vm.proposal.event_activity.id,
            }
            //this.$refs.edit_abseiling_climbing.abseiling_climbing=this.new_abseiling_climbing;
            this.$refs.edit_abseiling_climbing.abseiling_climbing=new_abseiling_climbing_another;
            this.$refs.edit_abseiling_climbing.abseiling_climbing_action='add'
            this.$refs.edit_abseiling_climbing.isModalOpen = true;
        },
        editRecord: function(id){
            this.$refs.edit_abseiling_climbing.abseiling_climbing_id = id;
            this.$refs.edit_abseiling_climbing.fetchRecord(id);
            this.$refs.edit_abseiling_climbing.isModalOpen = true;
        },
        discardRecord:function (abseiling_climbing_id) {
            let vm = this;
            swal({
                title: "Discard Record",
                text: "Are you sure you want to discard this record?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_abseiling_climbing(abseiling_climbing_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Record has been discarded',
                        'success'
                    )
                    vm.$refs.abseiling_climbing_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            vm.$refs.abseiling_climbing_datatable.vmDataTable.on('click', 'a[data-edit-abseiling_climbing]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-edit-abseiling_climbing');
                vm.editRecord(id);
            });
            // External Discard listener
            vm.$refs.abseiling_climbing_datatable.vmDataTable.on('click', 'a[data-discard-abseiling_climbing]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-abseiling_climbing');
                vm.discardRecord(id);
            });
        },
        refreshFromResponse: function(){
            this.$refs.abseiling_climbing_datatable.vmDataTable.ajax.reload();
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
            var column = vm.$refs.abseiling_climbing_datatable.vmDataTable.columns(8); //Hide 'Assigned To column for external'
            column.visible(false);
        }
        
    }
}
</script>
<style scoped>
</style>
