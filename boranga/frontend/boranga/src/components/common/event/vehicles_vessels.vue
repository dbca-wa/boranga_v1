<template lang="html">
<div class="row" id="vehiclesVesselsInfo">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Vehicles/Vessels <small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#vehiclesVesselsInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        
                        <div class="">
                            <!-- <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Hired or owned</label>
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  :value="true" data-parsley-required :disabled="proposal.readonly" name="vehicle_owned" v-model="proposal.event_vehicles_vessels.hired_or_owned"/>
                                            Owned
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  :value="false" data-parsley-required :disabled="proposal.readonly" name="vehicle_owned" v-model="proposal.event_vehicles_vessels.hired_or_owned"/>
                                            Hired
                                        </li>
                                    </ul>
                                </div>
                            </div> -->
                            <div class="row">&nbsp;</div>
                            <!-- <div class="" v-if="proposal.event_vehicles_vessels.hired_or_owned"> -->
                            <div class="">
                                <label class="">Provide details of every vehicle you plan to use when accessing the parks. 'Hire vehicle' can be entered as the vehicle registration if the hire vehicle details are not yet known.</label>
                                <VehicleTable :url="vehicles_url" :proposal="proposal" :access_types="access_types" ref="vehicles_table"></VehicleTable>
                            </div>
                            <div class="row">&nbsp;</div>
                        </div> 
                    </div>

                    <div class="form-horizontal col-sm-12 borderDecoration">
                        <label class="control-label">Provide details of every vessel you plan to use when accessing the parks for the event</label>
                        <VesselTable :url="vessels_url" :proposal="proposal" ref="vessel_table"></VesselTable>
                    </div>

                </div>
            </div>                

        </div>
    </div>

</div>
</template>

<script>
import {helpers,api_endpoints} from "@/utils/hooks.js"
import VehicleTable from '@/components/common/vehicle_table.vue'
import VesselTable from '@/components/common/vessel_table.vue'
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
                lBody: 'lBody'+vm._uid,
                values:null,
                access_types:[],
                vehicles_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.proposal_id+'/vehicles'),
                vessels_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.proposal_id+'/vessels'),
            }
        },
        components:{
            VehicleTable,
            VesselTable,
            //FileField,
        },
        methods:{
            fetchAccessTypes: function(){
                let vm = this;
                vm.$http.get(api_endpoints.access_types).then((response) => {
                    vm.access_types = response.body;
                    //console.log(vm.access_types);
                },(error) => {
                    console.log(error);
                } );
            },
        },
        mounted: function(){
            let vm=this;
            vm.fetchAccessTypes();
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

