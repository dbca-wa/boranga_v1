p<template lang="html">
<div class="row" id="approvalType">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Approval Type <small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#accessInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    

                    <div class="form-horizontal col-sm-12">
                        
                        <div class="form-group">
                            <div class="">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    This Application should result in a </label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_approval_type" value="lawful_authority" data-parsley-required :disabled="readonly" name="filming_approval_type"/>
                                            Lawful Authority
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_approval_type" value="licence" data-parsley-required :disabled="readonly" name="filming_approval_type"/>
                                            Licence
                                        </li>
                                    </ul>      
                                </div>
                            </div>  
                            <div class="row">&nbsp;</div>
                            <div v-if="proposal.filming_approval_type=='licence'" class="">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Filming licence charge type </label>
                                    
                                </div>
                                <div class="col-sm-6" style="margin-bottom: 5px">
                                    <select style="width:100%;" class="form-control input-sm" v-model="proposal.filming_licence_charge_type" ref="filming_licence_charge" :disabled="readonly">
                                        <option v-for="f in filming_licence_charge_choices" :value="f.key">{{f.value}}</option>
                                    </select>    
                                </div>
                            </div>  
                            <div class="row">&nbsp;</div>
                            <div v-if="proposal.filming_licence_charge_type=='non_standard_charge'" class="">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Non standard licence charge </label>
                                    
                                </div>
                                <!-- <div class="col-sm-6">
                                    <input type="number" :disabled="readonly" class="form-control" name="non_standard_charge" v-model="proposal.filming_non_standard_charge" min="0" step="0.01">   
                                </div> -->
                                <div class="col-sm-6">
                                    <input type="number" :disabled="readonly" class="form-control" name="non_standard_charge" v-model="proposal.filming_non_standard_charge" min="0.00" step="0.01" @blur="focusOut" placeholder="0.00">   
                                </div>
                            </div>  
                            <div class="row">&nbsp;</div>
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
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
    export default {
        props:{
            proposal:{
                type: Object,
                required:true
            },
            hasAssessorMode:{
                type:Boolean,
                default: false
            },
        },
        data:function () {
            let vm = this;
            return{
                lBody: 'lBody'+vm._uid,
                values:null,
                selected_approval_type:'',
                filming_licence_charge_choices:'',
                non_standard_charge: 0.00
            }
        },
        watch:{

            // non_standard_charge: function() {
            //     let vm = this;
            //     var total = 0.0;
                
            //     total = isNaN(parseFloat(vm.non_standard_charge)) ? 0.00 : parseFloat(vm.non_standard_charge);
            //     console.log(total.toFixed(2));
                
            //     this.non_standard_charge=total.toFixed(2);
            // },
        },
        computed:{
            readonly: function(){
                return !this.hasAssessorMode ? true : false;
            }
        },
        components:{
        },
        methods:{
            fetchLicenceChargeChoices: function(){
                let vm = this;
                vm.$http.get('/api/filming_licence_charge_choices').then((response) => {
                    vm.filming_licence_charge_choices=response.body
                },(error) => {
                    console.log(error);
                } );
            },
            focusOut: function() {
                let vm = this;
                var total = 0.0;
                
                total = isNaN(parseFloat(vm.proposal.filming_non_standard_charge)) ? 0.00 : parseFloat(vm.proposal.filming_non_standard_charge);
                console.log(total.toFixed(2));
                
                this.proposal.filming_non_standard_charge=total.toFixed(2);
            },
        },
        mounted: function(){
            this.selected_approval_type=this.proposal.filming_approval_type;
            this.fetchLicenceChargeChoices();
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

