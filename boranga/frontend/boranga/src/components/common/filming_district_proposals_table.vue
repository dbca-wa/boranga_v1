<template id="district_proposal_table">
    <div class="row">
        <div class="col-sm-12"> 
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">District Applications
                        <a :href="'#'+pBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="pBody">
                            <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                        </a>
                    </h3>
                </div>

                <div class="panel-body collapse in" :id="pBody">
                    <div class="row">
                        <div class="col-lg-12" style="margin-top:25px;">
                            <datatable ref="district_proposal_datatable" :id="datatable_id" :dtOptions="district_proposal_options" :dtHeaders="district_proposal_headers"/>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>
<script>
import datatable from '@/utils/vue/datatable.vue'
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'FilmingDistrictProposalTableDash',
    props: {
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
            pBody: 'pBody' + vm._uid,
            datatable_id: 'district-proposal-datatable-'+vm._uid,
            
            district_proposal_headers:["District","Status","Assigned Officer","Action"],
            district_proposal_options:{
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
                        data: "district_name",
                       
                    },
                    {
                        data: "processing_status",

                    },
                    {
                        data: "assigned_officer",
                    },
                    {
                        data: '',
                        mRender:function (data,type,full) {
                            let links = '';
                            
                           links +=  full.district_assessor_can_assess ? `<a href='/internal/proposal/${full.proposal}/district_proposal/${full.id}'>Process</a><br/>`: `<a href='/internal/proposal/${full.proposal}/district_proposal/${full.id}'>View</a><br/>`;
                        
                        
                            return links;
                        },
                        // name: ''  
                    },
                ],
                processing: true,
                
            }
        }
    },
    components:{
        datatable,
    },
    watch:{
    },
    computed: {

        is_external: function(){
            return this.level == 'external';
        },
    },
    methods:{
        fetchFilterLists: function(){
            let vm = this;

            // vm.$http.get(api_endpoints.filter_list_compliances).then((response) => {
            //     vm.district_proposal_regions = response.body.regions;
            //     vm.district_proposal_activityTitles = response.body.activities;
            //     vm.status = vm.level == 'external' ? vm.external_status: vm.internal_status;
            // },(error) => {
            //     console.log(error);
            // })
            //console.log(vm.regions);
        },
        addEventListeners: function(){
            
        },
        refreshFromResponse: function(){
            this.$refs.district_proposal_datatable.vmDataTable.ajax.reload();
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
       
    }
}
</script>
<style scoped>
</style>
