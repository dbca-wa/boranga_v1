<template lang="html">
<div class="row" id="equipmentInfo">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Vehicles, Vessels, RPA and other Equipment <small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#accessInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        
                        <div class="form-group col-sm-12" >
                            <div class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Are your vehicles </label>
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_equipment.vehicle_owned" :value="true" data-parsley-required :disabled="proposal.readonly" name="vehicle_owned"/>
                                            Owned
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_equipment.vehicle_owned" :value="false" data-parsley-required :disabled="proposal.readonly" name="vehicle_owned"/>
                                            Hired
                                        </li>
                                    </ul>  
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="" v-if="proposal.filming_equipment.vehicle_owned">
                                <!-- <label class="control-label">Provide details of every vehicle you plan to use when accessing the parks</label> -->
                                <VehicleTable :url="vehicles_url" :proposal="proposal" :access_types="access_types" ref="vehicles_table"></VehicleTable>
                            </div>
                        </div> 
                    </div>
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        <VesselTable :url="vessels_url" :proposal="proposal" ref="vessel_table"></VesselTable>
                    </div>

                    <div class="form-horizontal col-sm-12 borderDecoration">
                        <div class="row">&nbsp;</div>
                        <div class="row">
                            <div class="col-sm-6">
                                <label class="control-label pull-right"  for="Name">Are you using a Remotely Piloted Aircraft (RPA) for your filming and/or photography activities?</label>
                            </div>
                            <div class="col-sm-6" style="margin-bottom: 5px">
                                <ul class="list-inline"  >
                                    <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_equipment.rps_used" :value="true" data-parsley-required :disabled="proposal.readonly" name="rps_used"/>
                                            Yes
                                    </li>
                                    <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_equipment.rps_used" :value="false" data-parsley-required :disabled="proposal.readonly" name="rps_used"/>
                                            No
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="row">&nbsp;</div>
                        <div class="row" v-if="proposal.filming_equipment.rps_used">
                            <!-- <div class="col-sm-6">
                                <label class="control-label pull-right"  for="Name">Does the RPA weigh over two kilograms?</label>
                            </div>
                            <div class="col-sm-6" style="margin-bottom: 5px">
                                <ul class="list-inline"  >
                                    <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_equipment.rps_overweight" :value="true" data-parsley-required :disabled="proposal.readonly" name="rps_overweight"/>
                                            Yes
                                    </li>
                                    <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_equipment.rps_overweight" :value="false" data-parsley-required :disabled="proposal.readonly" name="rps_overweight"/>
                                            No
                                    </li>
                                </ul>
                            </div> -->
                            <div class="col-sm-6">
                                    <label class="control-label pull-right"  for="Name">
                                    Please specify the model of RPA you intend to use and attach a copy of your CASA remotely piloted aircraft operator accreditation or licence (RePL) and operator's certificate (ReOC) </label>
                                    
                            </div>
                            <div class="col-sm-6" style="margin-bottom: 5px">
                                    <div class="col-sm-6" style="margin-bottom: 5px">
                                      <textarea :disabled="readonly" class="form-control" name="camp_location" placeholder="" v-model="proposal.filming_equipment.rps_used_details" :disabled="proposal.readonly"></textarea>
                                    </div>    
                            </div>
                        </div>
                        <div class="row" v-if="proposal.filming_equipment.rps_used">
                                
                                <div class="col-sm-6">
                                    <label class="control-label pull-right"  for="Name">
                                    Attach document</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <div class="col-sm-6" style="margin-bottom: 5px">
                                        <FileField :proposal_id="proposal.id" isRepeatable="true" name="rps_certificate" :id="'proposal'+proposal.id" :readonly="proposal.readonly" ref="rps_certificate"></FileField>
                                    </div>
                                </div>                                
                        </div>
                        <div class="row">&nbsp;</div>
                        <!-- <div class="row" v-if="proposal.filming_equipment.rps_used && proposal.filming_equipment.rps_overweight">
                            <div class="col-sm-6">
                                <label class="control-label pull-right"  for="Name">Attach CASA Remotely piloted aircraft operator's certificate (ReOC) or licence (RePL)</label>
                            </div>
                            <div class="col-sm-6" style="margin-bottom: 5px">
                                <div class="col-sm-6" style="margin-bottom: 5px">
                                      <FileField :proposal_id="proposal.id" isRepeatable="false" name="rps_certificate" :id="'proposal'+proposal.id" :readonly="proposal.readonly" ref="rps_cert"></FileField>  
                                </div>
                            </div>
                        </div> -->
                    </div>

                    <div class="form-horizontal col-sm-12 borderDecoration">
                        <div class="row">&nbsp;</div>
                        <div class="row">
                            <div class="col-sm-6">
                                <label class="control-label pull-right"  for="Name">Number and type of cameras to be used </label>
                            </div>
                            <div class="col-sm-6" style="margin-bottom: 5px">
                                <div class="col-sm-6" style="margin-bottom: 5px">
                                      <!-- <input type="text" class="form-control" name="num_cameras" placeholder="" :disabled="proposal.readonly" v-model="proposal.filming_equipment.num_cameras"> -->
                                      <textarea type="text" class="form-control" name="num_cameras" placeholder="" :disabled="proposal.readonly" v-model="proposal.filming_equipment.num_cameras" :disabled="proposal.readonly"></textarea>   
                                </div>
                            </div>
                        </div>
                        <div class="row">&nbsp;</div>
                        <div class="row">
                            <div class="col-sm-6">
                                <label class="control-label pull-right"  for="Name">Will any stuctures or facilities be erected or does the area require any alteration to occur to allow the filming?</label>
                            </div>
                            <div class="col-sm-6" style="margin-bottom: 5px">
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                                <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_equipment.alteration_required" :value="true" data-parsley-required :disabled="proposal.readonly" name="alteration_required"/>
                                                Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                                <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_equipment.alteration_required" :value="false" data-parsley-required :disabled="proposal.readonly" name="alteration_required"/>
                                                No
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="row">&nbsp;</div>
                        <div v-if="proposal.filming_equipment.alteration_required" class="row">
                                <div class="col-sm-6">
                                    <label class="control-label pull-right"  for="Name">
                                    Please provide details and/or attach a copy of the plans or specifications </label>
                                    
                                </div>
                                <div class="col-sm-6" style="margin-bottom: 5px">
                                    <div class="col-sm-6" style="margin-bottom: 5px">
                                      <textarea :disabled="readonly" class="form-control" name="camp_location" placeholder="" v-model="proposal.filming_equipment.alteration_required_details" :disabled="proposal.readonly"></textarea>
                                    </div>    
                                </div>
                        </div>
                        <div class="row" v-if="proposal.filming_equipment.alteration_required">
                                
                                <div class="col-sm-6">
                                    <label class="control-label pull-right"  for="Name">
                                    Attach document</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <div class="col-sm-6" style="margin-bottom: 5px">
                                        <FileField :proposal_id="proposal.id" isRepeatable="true" name="alteration_required" :id="'proposal'+proposal.id" :readonly="proposal.readonly"></FileField>
                                    </div>
                                </div>                                
                        </div>
                            
                        <div class="row">&nbsp;</div>
                        <div class="row">
                            <div class="col-sm-6">
                                <label class="control-label pull-right"  for="Name">List any other significant equipment that may be used during the proposed operations</label>
                            </div>
                            <div class="col-sm-6" style="margin-bottom: 5px">
                                <div class="col-sm-6" style="margin-bottom: 5px">
                                      <textarea type="text" class="form-control" name="num_cameras" placeholder="" :disabled="proposal.readonly" v-model="proposal.filming_equipment.other_equipments" :disabled="proposal.readonly"></textarea>   
                                </div>
                            </div>
                        </div>
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
import FileField from '@/components/forms/filefield.vue' 
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
            FileField,
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

