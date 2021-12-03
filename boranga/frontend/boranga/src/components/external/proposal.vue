<template lang="html">
    <div class="container" >
        <form :action="proposal_form_url" method="post" name="new_proposal" enctype="multipart/form-data">
            <div v-if="!proposal_readonly">
              <div v-if="hasAmendmentRequest" class="row" style="color:red;">
                  <div class="col-lg-12 pull-right">
                    <div class="panel panel-default">
                      <div class="panel-heading">
                        <h3 class="panel-title" style="color:red;">An amendment has been requested for this Application
                          <a class="panelClicker" :href="'#'+pBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="pBody">
                                <span class="glyphicon glyphicon-chevron-down pull-right "></span>
                          </a>
                        </h3>
                      </div>
                      <div class="panel-body collapse in" :id="pBody">
                        <div v-for="a in amendment_request">
                          <p>Reason: {{a.reason}}</p>
                          <p>Details: <p v-for="t in splitText(a.text)">{{t}}</p></p>  
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div id="error" v-if="missing_fields.length > 0" style="margin: 10px; padding: 5px; color: red; border:1px solid red;">
                <b>Please answer the following mandatory question(s):</b>
                <ul>
                    <li v-for="error in missing_fields">
                        {{ error.label }}
                    </li>
                </ul>
            </div>

            <div v-if="proposal" id="scrollspy-heading" class="col-lg-12" >
                <h4>Commercial Operator - {{proposal.application_type}} application: {{proposal.lodgement_number}}</h4>
            </div>

            <ProposalTClass v-if="proposal && proposal_parks && proposal.application_type==application_type_tclass" :proposal="proposal" id="proposalStart"  :canEditActivities="canEditActivities" :is_external="true" :proposal_parks="proposal_parks" ref="proposal_tclass"></ProposalTClass>
            <ProposalFilming v-else-if="proposal && proposal.application_type==application_type_filming" :proposal="proposal" id="proposalStart" :canEditActivities="canEditActivities" :canEditPeriod="canEditPeriod" :is_external="true" :proposal_parks="proposal_parks" ref="proposal_filming"></ProposalFilming>
            <ProposalEvent v-else-if="proposal && proposal.application_type==application_type_event" :proposal="proposal" id="proposalStart" :canEditActivities="canEditActivities" :canEditPeriod="canEditPeriod" :is_external="true" :proposal_parks="proposal_parks" ref="proposal_event"></ProposalEvent>

            <div>
                <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token"/>
                <input type='hidden' name="schema" :value="JSON.stringify(proposal)" />
                <input type='hidden' name="proposal_id" :value="1" />

                <div class="row" style="margin-bottom: 50px">
                        <div  class="container">
                          <div class="row" style="margin-bottom: 50px">
                              <div class="navbar navbar-fixed-bottom"  style="background-color: #f5f5f5;">
                                  <div class="navbar-inner">
                                    <div v-if="proposal && !proposal.readonly" class="container">
                                      <p class="pull-right" style="margin-top:5px">
                                        <button v-if="saveExitProposal" type="button" class="btn btn-primary" disabled>Save and Exit&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <input v-else type="button" @click.prevent="save_exit" class="btn btn-primary" value="Save and Exit" :disabled="savingProposal || paySubmitting"/>
                                        <button v-if="savingProposal" type="button" class="btn btn-primary" disabled>Save and Continue&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <input v-else type="button" @click.prevent="save" class="btn btn-primary" value="Save and Continue" :disabled="saveExitProposal || paySubmitting"/>

                                        <button v-if="paySubmitting" type="button" class="btn btn-primary" disabled>{{ submit_text() }}&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i></button>
                                        <!-- <input v-else type="button" @click.prevent="submit" class="btn btn-primary" :value="submit_text()" :disabled="!proposal.training_completed || saveExitProposal || savingProposal"/> -->
                                        <input v-else type="button" @click.prevent="submit" class="btn btn-primary" :value="submit_text()" :disabled="!trainingCompleted || saveExitProposal || savingProposal"/>
                                        <input id="save_and_continue_btn" type="hidden" @click.prevent="save_wo_confirm" class="btn btn-primary" value="Save Without Confirmation"/>
                                      </p>
                                    </div>
                                    <div v-else class="container">
                                      <p class="pull-right" style="margin-top:5px;">
                                        <router-link class="btn btn-primary" :to="{name: 'external-proposals-dash'}">Back to Dashboard</router-link>
                                      </p>
                                    </div>
                                  </div>
                                </div>
                            </div>
                        </div>
                </div>
            </div>

        </form>
    </div>
</template>
<script>
//import Proposal from '../form.vue'
import ProposalTClass from '../form_tclass.vue'
import ProposalFilming from '../form_filming.vue'
import ProposalEvent from '../form_event.vue'
import Vue from 'vue' 
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
  name: 'ExternalProposal',
  data: function() {
    return {
      "proposal": null,
      "loading": [],
      form: null,
      amendment_request: [],
      //isDataSaved: false,
      saveError: false,
      proposal_readonly: true,
      hasAmendmentRequest: false,
      submitting: false,
      saveExitProposal: false,
      savingProposal:false,
      paySubmitting:false,
      newText: "",
      pBody: 'pBody',
      missing_fields: [],
      proposal_parks:null,
    }
  },
  components: {
      ProposalTClass,
      ProposalFilming,
      ProposalEvent
  },
  computed: {
    isLoading: function() {
      return this.loading.length > 0
    },
    csrf_token: function() {
      return helpers.getCookie('csrftoken')
    },
    proposal_form_url: function() {
      return (this.proposal) ? `/api/proposal/${this.proposal.id}/draft.json` : '';
    },
    application_fee_url: function() {
      return (this.proposal) ? `/application_fee/${this.proposal.id}/` : '';
    },
    proposal_submit_url: function() {
      return (this.proposal) ? `/api/proposal/${this.proposal.id}/submit.json` : '';
      //return this.submit();
    },
    canEditActivities: function(){
      return this.proposal ? this.proposal.can_user_edit: 'false';
    },
    canEditPeriod: function(){
      return this.proposal ? this.proposal.can_user_edit: 'false';
    },
    application_type_tclass: function(){
      return api_endpoints.t_class;
    },
    application_type_filming: function(){
      return api_endpoints.filming;
    },
    application_type_event: function(){
      return api_endpoints.event;
    },
    trainingCompleted: function(){
      if(this.proposal.application_type== 'Event')
        {
          return this.proposal.applicant_training_completed;
        }
      return this.proposal.training_completed;
    }

  },
  methods: {
    proposal_refs:function(){
      let vm=this;
      if(vm.proposal.application_type == vm.application_type_tclass) {
          return vm.$refs.proposal_tclass;
      } else if(vm.proposal.application_type == vm.application_type_filming) {
          return vm.$refs.proposal_filming;
      } else if(vm.proposal.application_type == vm.application_type_event) {
          return vm.$refs.proposal_event;
      }
    },

    submit_text: function() {
      let vm = this;
      //return vm.proposal.fee_paid ? 'Resubmit' : 'Pay and Submit';
      if (vm.proposal.application_type==vm.application_type_filming) {
          // Filming has deferred payment once assessor decides whether 'Licence' (has a fee) or 'Lawful Authority' (has no fee) is to be issued
          return 'Submit';
      } else if (vm.proposal.fee_paid) {
          return 'Resubmit';
      } else if (vm.proposal.allow_full_discount)  {
          return 'Submit';
      } else {
          return 'Pay and Submit';
      }
    },
    _save_applicant_data:function(){
      let vm=this;
      let proposal_type = vm.$refs.proposal_tclass
      if(vm.proposal.applicant_type == 'SUB')
      {
        vm.$refs.proposal_tclass.$refs.profile.updatePersonal();
        vm.$refs.proposal_tclass.$refs.profile.updateAddress();
        vm.$refs.proposal_tclass.$refs.profile.updateContact();
      }
      if(vm.proposal.applicant_type == 'ORG'){
        vm.$refs.proposal_tclass.$refs.organisation.updateDetails_noconfirm();
        //vm.$refs.proposal_tclass.$refs.organisation.updateDetails();
        vm.$refs.proposal_tclass.$refs.organisation.updateAddress();
      }
    },
    save_applicant_data:function(){
      let vm=this;
      if(vm.proposal.applicant_type == 'SUB')
      {
        vm.proposal_refs().$refs.profile.updatePersonal();
        vm.proposal_refs().$refs.profile.updateAddress();
        vm.proposal_refs().$refs.profile.updateContact();
      }
      if(vm.proposal.applicant_type == 'ORG'){
        vm.proposal_refs().$refs.organisation.updateDetails();
        vm.proposal_refs().$refs.organisation.updateAddress();
      }
    },


    set_formData: function(e) {
      let vm = this;
      //vm.form=document.forms.new_proposal;
      let formData = new FormData(vm.form);

      //console.log('land activities', vm.proposal.selected_parks_activities);
      formData.append('selected_parks_activities', JSON.stringify(vm.proposal.selected_parks_activities))
      formData.append('selected_trails_activities', JSON.stringify(vm.proposal.selected_trails_activities))
      formData.append('marine_parks_activities', JSON.stringify(vm.proposal.marine_parks_activities))

      return formData;
    },
    save: function(e) {
      let vm = this;
      vm.savingProposal=true;
      vm.save_applicant_data();

      let formData = vm.set_formData()
      vm.$http.post(vm.proposal_form_url,formData).then(res=>{
          swal(
            'Saved',
            'Your application has been saved',
            'success'
          );
          vm.savingProposal=false;
      },err=>{
        var errorText=helpers.apiVueResourceError(err); 
                  swal(
                          'Save Error',
                          //helpers.apiVueResourceError(err),
                          errorText,
                          'error'
                      )
        vm.savingProposal=false;
      });
    },
    save_exit: function(e) {
      let vm = this;
      this.submitting = true;
      this.saveExitProposal=true;
      this.save(e);
      this.saveExitProposal=false;
      // redirect back to dashboard
      vm.$router.push({
        name: 'external-proposals-dash'
      });
    },

    save_wo_confirm: function(e) {
      let vm = this;
      vm.save_applicant_data();
      let formData = vm.set_formData()

      vm.$http.post(vm.proposal_form_url,formData);
    },
    save_before_submit: async function(e) {
      //console.log('save before submit');
      let vm = this;
      vm.save_applicant_data();
      let formData = vm.set_formData()
      vm.saveError=false;

      //vm.$http.post(vm.proposal_form_url,formData);
      const result = await vm.$http.post(vm.proposal_form_url,formData).then(res=>{
          //return true;
      },err=>{
                  var errorText=helpers.apiVueResourceError(err); 
                  swal(
                          'Submit Error',
                          //helpers.apiVueResourceError(err),
                          errorText,
                          'error'
                      )
                  vm.paySubmitting=false;
                  vm.saveError=true;
        //return false;
      });
      return result;
    },

    save_and_redirect: function(e) {
      let vm = this;
      let formData = vm.set_formData()

      vm.save_applicant_data();
      vm.$http.post(vm.proposal_form_url,formData).then(res=>{
          /* after the above save, redirect to the Django post() method in ApplicationFeeView */
          vm.post_and_redirect(vm.application_fee_url, {'csrfmiddlewaretoken' : vm.csrf_token});
      },err=>{
        var errorText=helpers.apiVueResourceError(err); 
                  swal(
                          'Submit Error',
                          //helpers.apiVueResourceError(err),
                          errorText,
                          'error'
                      )
                  vm.paySubmitting=false;
      });
    },

    setdata: function(readonly){
      this.proposal_readonly = readonly;
    },

    setAmendmentData: function(amendment_request){
      this.amendment_request = amendment_request;
      
      if (amendment_request.length > 0)
        this.hasAmendmentRequest = true;
        
    },

    splitText: function(aText){
      let newText = '';
      newText = aText.split("\n");
      return newText;

    },

    leaving: function(e) {
      let vm = this;
      var dialogText = 'You have some unsaved changes.';
      if (!vm.proposal_readonly && !vm.submitting){
        e.returnValue = dialogText;
        return dialogText;
      }
      else{
        return null;
      }
    },
    
    highlight_missing_fields: function(){
        let vm = this;
        for (var missing_field of vm.missing_fields) {
            $("#" + missing_field.id).css("color", 'red');
        }
    },

    validate: function(){
        let vm = this;

        // reset default colour
        for (var field of vm.missing_fields) {
            $("#" + field.id).css("color", '#515151');
        }
        vm.missing_fields = [];

        // get all required fields, that are not hidden in the DOM
        //var hidden_fields = $('input[type=text]:hidden, textarea:hidden, input[type=checkbox]:hidden, input[type=radio]:hidden, input[type=file]:hidden');
        //hidden_fields.prop('required', null);
        //var required_fields = $('select:required').not(':hidden');
        var required_fields = $('input[type=text]:required, textarea:required, input[type=checkbox]:required, input[type=radio]:required, input[type=file]:required, select:required').not(':hidden');

        // loop through all (non-hidden) required fields, and check data has been entered
        required_fields.each(function() {
            //console.log('type: ' + this.type + ' ' + this.name)
            var id = 'id_' + this.name
            if (this.type == 'radio') {
                //if (this.type == 'radio' && !$("input[name="+this.name+"]").is(':checked')) {
                if (!$("input[name="+this.name+"]").is(':checked')) {
                    var text = $('#'+id).text()
                    console.log('radio not checked: ' + this.type + ' ' + text)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'checkbox') {
                //if (this.type == 'radio' && !$("input[name="+this.name+"]").is(':checked')) {
                var id = 'id_' + this.classList['value']
                if ($("[class="+this.classList['value']+"]:checked").length == 0) {
                    var text = $('#'+id).text()
                    console.log('checkbox not checked: ' + this.type + ' ' + text)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'select-one') {
                if ($(this).val() == '') {
                    var text = $('#'+id).text()  // this is the (question) label
                    var id = 'id_' + $(this).prop('name'); // the label id
                    console.log('selector not selected: ' + this.type + ' ' + text)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'file') {
                var num_files = $('#'+id).attr('num_files')
                if (num_files == "0") {
                    var text = $('#'+id).text()
                    console.log('file not uploaded: ' + this.type + ' ' + this.name)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'text') {
                if (this.value == '') {
                    var text = $('#'+id).text()
                    console.log('text not provided: ' + this.type + ' ' + this.name)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'textarea') {
                if (this.value == '') {
                    var text = $('#'+id).text()
                    console.log('textarea not provided: ' + this.type + ' ' + this.name)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            /*
            if (this.type == 'select') {
                if (this.value == '') {
                    var text = $('#'+id).text()
                    console.log('select not provided: ' + this.type + ' ' + this.name)
                    vm.missing_fields.push({id: id, label: text});
                }
            }

            if (this.type == 'multi-select') {
                if (this.value == '') {
                    var text = $('#'+id).text()
                    console.log('multi-select not provided: ' + this.type + ' ' + this.name)
                    vm.missing_fields.push({id: id, label: text});
                }
            }
            */



        });

        return vm.missing_fields.length
    },

    can_submit: function(){
      let vm=this;
      let blank_fields=[]

      if (vm.proposal.application_type==vm.application_type_tclass) {
          if (vm.$refs.proposal_tclass.$refs.other_details.selected_accreditations.length==0 ){
            blank_fields.push(' Level of Accreditation is required')
          }
          else{
            for(var i=0; i<vm.proposal.other_details.accreditations.length; i++){
              if(!vm.proposal.other_details.accreditations[i].is_deleted && vm.proposal.other_details.accreditations[i].accreditation_type!='no'){
                if(vm.proposal.other_details.accreditations[i].accreditation_expiry==null || vm.proposal.other_details.accreditations[i].accreditation_expiry==''){
                  blank_fields.push('Expiry date for accreditation type '+vm.proposal.other_details.accreditations[i].accreditation_type_value+' is required')
                }
                // var acc_doc_ref='accreditation_file'+vm.proposal.other_details.accreditations[i].accreditation_type;
                var acc_ref= vm.proposal.other_details.accreditations[i].accreditation_type;
                // console.log(acc_doc_ref, acc_ref);
                if(vm.$refs.proposal_tclass.$refs.other_details.$refs[acc_ref][0].$refs.accreditation_file.documents.length==0){
                  blank_fields.push('Accreditation Certificate for accreditation type '+vm.proposal.other_details.accreditations[i].accreditation_type_value+' is required')
                }

              }
            }
          }

          if (vm.proposal.other_details.preferred_licence_period=='' || vm.proposal.other_details.preferred_licence_period==null ){
            blank_fields.push(' Preferred Licence Period is required')
          }
          if (vm.proposal.other_details.nominated_start_date=='' || vm.proposal.other_details.nominated_start_date==null ){
            blank_fields.push(' Licence Nominated Start Date is required')
          }

          if(vm.$refs.proposal_tclass.$refs.other_details.$refs.deed_poll_doc.documents.length==0){
            blank_fields.push(' Deed poll document is missing')
          }

          if(vm.$refs.proposal_tclass.$refs.other_details.$refs.currency_doc.documents.length==0){
            blank_fields.push(' Certificate of currency document is missing')
          }
          if(vm.proposal.other_details.insurance_expiry=='' || vm.proposal.other_details.insurance_expiry==null){
            blank_fields.push(' Certificate of currency expiry date is missing')
          }

      } else if (vm.proposal.application_type==vm.application_type_filming) {
          // if (vm.proposal.filming_activity.commencement_date =='' || vm.proposal.filming_activity.commencement_date ==null || vm.proposal.filming_activity.completion_date =='' || vm.proposal.filming_activity.completion_date ==''){
          //   blank_fields.push(' Period of proposed filming/ photography is required')
          // }
          // if(vm.proposal.filming_activity.film_type=='' || vm.proposal.filming_activity.film_type==null){
          //   blank_fields.push(' Type of film to be undertaken is missing')
          // }
          blank_fields=vm.can_submit_filming()

      } else if (vm.proposal.application_type==vm.application_type_event) {
          blank_fields=vm.can_submit_event();

      }

      if(blank_fields.length==0){
        return true;
      }
      else{
        return blank_fields;
      }

    },
    can_submit_event: function(){
      let vm=this;
      let blank_fields=[]

      if(vm.proposal.event_activity.event_name==''||vm.proposal.event_activity.event_name==null){
        blank_fields.push(' Name of the event is missing')
      }
      if(vm.proposal.event_activity.commencement_date =='' || vm.proposal.event_activity.commencement_date ==null || vm.proposal.event_activity.completion_date =='' || vm.proposal.event_activity.completion_date ==''){
        blank_fields.push(' Period of proposed event is required')

      }
      if(vm.proposal.event_activity.completion_date != '' && vm.proposal.event_activity.max_num_months_ahead != 0) {
           let completion_date = moment(vm.proposal.event_activity.completion_date, 'DD/MM/YYYY');
           let max_future_date = moment().add(vm.proposal.event_activity.max_num_months_ahead, 'months');
           if(completion_date > max_future_date ) {
              blank_fields.push(' Event Completion Date cannot be beyond ' + max_future_date.format("DD-MM-YYYY"))
           }
      }
      if(vm.$refs.proposal_event.$refs.event_activities.$refs.parks_table.$refs.event_park_maps.documents.length==0){
            blank_fields.push(' A detailed itinerary and map of the event route document is missing')
      }
      if(vm.proposal.event_activity.pdswa_location){
        if(vm.$refs.proposal_event.$refs.event_activities.$refs.event_activity_pdswa_file.documents.length==0){
            blank_fields.push(' Department of Water and Environmental Regulation application form document is missing')
          }
      }
      if(vm.proposal.event_management.num_spectators==null||vm.proposal.event_management.num_spectators==''){
        blank_fields.push(' Number of spectators expected is missing')
      }
      if(vm.proposal.event_management.num_officials==null||vm.proposal.event_management.num_officials==''){
        blank_fields.push(' Number of officials expected is missing')
      }
      if(vm.proposal.event_management.num_vehicles==null||vm.proposal.event_management.num_vehicles==''){
        blank_fields.push(' Number of vehicles/ vessels is missing')
      }
      if(vm.proposal.event_management.media_involved){
        if(vm.proposal.event_management.media_details==null||vm.proposal.event_management.media_details==''){
          blank_fields.push(' Media involved details are missing')
        }
      }
      if(vm.proposal.event_management.structure_change){
        if(vm.proposal.event_management.structure_change_details==null||vm.proposal.event_management.structure_change_details==''){
          blank_fields.push(' Structure change details are missing')
        }
      }
      if(vm.proposal.event_management.vendor_hired){
        if(vm.proposal.event_management.vendor_hired_details==null||vm.proposal.event_management.vendor_hired_details==''){
          blank_fields.push(' Vendors hired details are missing')
        }
      }
      if(vm.proposal.event_management.toilets_provided){
        if(vm.proposal.event_management.toilets_provided_details==null||vm.proposal.event_management.toilets_provided_details==''){
          blank_fields.push(' Portable toilets and/ or showers details are missing')
        }
      }
      if(vm.proposal.event_management.rubbish_removal_details==null||vm.proposal.event_management.rubbish_removal_details==''){
          blank_fields.push(' Remove waste details are missing')
      }
      if(vm.proposal.event_management.approvals_gained){
        if(vm.proposal.event_management.approvals_gained_details==null||vm.proposal.event_management.approvals_gained_details==''){
          blank_fields.push(' Necessary approvals gained details are missing')
        }
        // if(vm.$refs.proposal_event.$refs.event_management.$refs.event_risk_management_plan.documents.length==0){
        //     blank_fields.push(' Necessary approvals gained document missing')
        //   }
      }
      if(vm.$refs.proposal_event.$refs.event_management.$refs.event_risk_management_plan.documents.length==0){
            // blank_fields.push(' Necessary approvals gained document missing')
            blank_fields.push(' Attached copies of your management plans are missing')
        }
      if(vm.proposal.event_management.traffic_management_plan){
        if(vm.$refs.proposal_event.$refs.event_management.$refs.event_management_traffic_management_plan.documents.length==0){
            blank_fields.push(' Traffic management plan document missing')
          }
      }
      if(vm.$refs.proposal_event.$refs.event_other_details.$refs.deed_poll_doc.documents.length==0){
          blank_fields.push(' Deed poll document is missing')
      }

      if(vm.$refs.proposal_event.$refs.event_other_details.$refs.currency_doc.documents.length==0){
          blank_fields.push(' Certificate of currency document is missing')
      }
      if(vm.proposal.event_other_details.insurance_expiry=='' || vm.proposal.event_other_details.insurance_expiry==null){
          blank_fields.push(' Certificate of currency expiry date is missing')
      }
      return blank_fields;
    },
    can_submit_filming: function(){
      let vm=this;
      let blank_fields=[]
      if (vm.proposal.filming_activity.commencement_date =='' || vm.proposal.filming_activity.commencement_date ==null || vm.proposal.filming_activity.completion_date =='' || vm.proposal.filming_activity.completion_date ==''){
          blank_fields.push(' Period of proposed filming/ photography is required')
      }
      if(vm.proposal.filming_activity.film_type=='' || vm.proposal.filming_activity.film_type==null){
          blank_fields.push(' Type of film to be undertaken is missing')
      }
      if(vm.proposal.filming_activity.activity_title=='' || vm.proposal.filming_activity.activity_title==null){
          blank_fields.push(' Title of film is missing')
      }
      if(vm.proposal.filming_activity.sponsorship=='' || vm.proposal.filming_activity.sponsorship==null){
          blank_fields.push(' Tourism WA sponsorship is missing')
      }
      if(vm.proposal.filming_activity.production_description=='' || vm.proposal.filming_activity.production_description==null){
          blank_fields.push(' Description of production is missing')
      }
      if(vm.proposal.filming_activity.film_purpose=='' || vm.proposal.filming_activity.film_purpose==null){
          blank_fields.push(' Film purpose is missing')
      }
      if(vm.proposal.filming_activity.film_usage=='' || vm.proposal.filming_activity.film_usage==null){
          blank_fields.push(' Usage of film is missing')
      }
      if(vm.proposal.filming_access.track_use){
        if(vm.proposal.filming_access.track_use_details=='' || vm.proposal.filming_access.track_use_details==null){
          blank_fields.push(' Track use details are missing')
        }
      }
      if(vm.proposal.filming_access.off_road){
        if(vm.proposal.filming_access.off_road_details=='' || vm.proposal.filming_access.off_road_details==null){
          blank_fields.push(' Off road details are missing')
        }
      }
      if(vm.proposal.filming_access.road_closure){
        if(vm.proposal.filming_access.road_closure_details=='' || vm.proposal.filming_access.road_closure_details==null){
          blank_fields.push(' Roads or car park to be closed details are missing')
        }
      }
      if(vm.proposal.filming_access.camp_on_land){
        if(vm.proposal.filming_access.camp_location=='' || vm.proposal.filming_access.camp_location==null){
          blank_fields.push(' Camping location details are missing')
        }
      }
      if(vm.proposal.filming_access.staff_assistance){
        if(vm.proposal.filming_access.assistance_staff_capacity=='' || vm.proposal.filming_access.assistance_staff_capacity==null){
          blank_fields.push(' Staff assistance capacity details are missing')
        }
      }
      if(vm.proposal.filming_access.staff_to_film){
        if(vm.proposal.filming_access.film_staff_capacity=='' || vm.proposal.filming_access.film_staff_capacity==null){
          blank_fields.push(' Department staff to film capacity details are missing')
        }
      }
      if(vm.proposal.filming_access.cultural_significance){
        if(vm.proposal.filming_access.cultural_significance_details=='' || vm.proposal.filming_access.cultural_significance_details==null){
          blank_fields.push(' Items/ areas of cultural significance details are missing')
        }
      }
      if(vm.proposal.filming_access.no_of_people=='' || vm.proposal.filming_access.no_of_people==null){
          blank_fields.push(' Number of people in filming party is missing')
      }
      if(vm.proposal.filming_equipment.rps_used){
        if(vm.proposal.filming_equipment.rps_used_details=='' || vm.proposal.filming_equipment.rps_used_details==null){
          blank_fields.push(' RPA details are missing')
        }
        if(vm.$refs.proposal_filming.$refs.filming_equipment.$refs.rps_certificate.documents.length==0){
            blank_fields.push(' RePL/ ReOC document missing')
          }
      }
      if(vm.proposal.filming_equipment.alteration_required){
        if(vm.proposal.filming_equipment.alteration_required_details=='' || vm.proposal.filming_equipment.alteration_required_details==null){
          blank_fields.push(' Any alteration to occur details are missing')
        }
      }
      if(vm.proposal.filming_equipment.num_cameras=='' || vm.proposal.filming_equipment.num_cameras==null){
          blank_fields.push(' Number and type of cameras is missing')
      }
      if(vm.proposal.filming_equipment.other_equipments=='' || vm.proposal.filming_equipment.other_equipments==null){
          blank_fields.push(' Other significant equipment details are missing')
      }
      if(vm.proposal.filming_other_details.safety_details=='' || vm.proposal.filming_other_details.safety_details==null){
          blank_fields.push(' Safety details are missing')
      }
      if(vm.$refs.proposal_filming.$refs.filming_other_details.$refs.currency_doc.documents.length==0){
          blank_fields.push(' Certificate of currency document is missing')
      }
      if(vm.proposal.filming_other_details.insurance_expiry=='' || vm.proposal.filming_other_details.insurance_expiry==null){
          blank_fields.push(' Certificate of currency expiry date is missing')
      }
      if(vm.$refs.proposal_filming.$refs.filming_other_details.$refs.deed_poll_doc.documents.length==0){
          blank_fields.push(' Deed poll document is missing')
      }
      return blank_fields
    },
    submit: function(){
        let vm = this;
        let formData = vm.set_formData()

        var missing_data= vm.can_submit();
        if(missing_data!=true){
          swal({
            title: "Please fix following errors before submitting",
            text: missing_data,
            type:'error'
          })
          //vm.paySubmitting=false;
          return false;
        }

        // remove the confirm prompt when navigating away from window (on button 'Submit' click)
        vm.submitting = true;
        vm.paySubmitting=true;

        swal({
            title: vm.submit_text() + " Application",
            text: "Are you sure you want to " + vm.submit_text().toLowerCase()+ " this application?",
            type: "question",
            showCancelButton: true,
            confirmButtonText: vm.submit_text()
        }).then(async () => {
          
            // Filming has deferred payment once assessor decides whether 'Licence' (fee) or 'Lawful Authority' (no fee) is to be issued
            // if (!vm.proposal.fee_paid || vm.proposal.application_type!='Filming') {
            if (!vm.proposal.fee_paid && vm.proposal.application_type!=vm.application_type_filming) {
                vm.save_and_redirect();

            } else {
                /* just save and submit - no payment required (probably application was pushed back by assessor for amendment */
                // var saved=true;
                //vm.save_wo_confirm()
                let result = await vm.save_before_submit()
                //vm.save_before_submit();
                //console.log(result);
                if(!vm.saveError){
                  vm.$http.post(helpers.add_endpoint_json(api_endpoints.proposals,vm.proposal.id+'/submit'),formData).then(res=>{
                      vm.proposal = res.body;
                      vm.$router.push({
                          name: 'submit_proposal',
                          params: { proposal: vm.proposal}
                      });
                  },err=>{
                      swal(
                          'Submit Error',
                          helpers.apiVueResourceError(err),
                          'error'
                      )
                  });
                }
            }
        },(error) => {
          vm.paySubmitting=false;
        });
        //vm.paySubmitting=false;
    },

    post_and_redirect: function(url, postData) {
        /* http.post and ajax do not allow redirect from Django View (post method), 
           this function allows redirect by mimicking a form submit.

           usage:  vm.post_and_redirect(vm.application_fee_url, {'csrfmiddlewaretoken' : vm.csrf_token});
        */
        var postFormStr = "<form method='POST' action='" + url + "'>";

        for (var key in postData) {
            if (postData.hasOwnProperty(key)) {
                postFormStr += "<input type='hidden' name='" + key + "' value='" + postData[key] + "'>";
            }
        }
        postFormStr += "</form>";
        var formElement = $(postFormStr);
        $('body').append(formElement);
        $(formElement).submit();
    },
    fetchProposalParks: function(proposal_id){
      let vm=this;
      vm.$http.get(helpers.add_endpoint_json(api_endpoints.proposals,proposal_id+'/parks_and_trails')).then(response => {
                vm.proposal_parks = helpers.copyObject(response.body);
                console.log(vm.proposal_parks)
            },
              error => {
            });

    },

  },

  mounted: function() {
    let vm = this;
    vm.form = document.forms.new_proposal;
    window.addEventListener('beforeunload', vm.leaving);
    window.addEventListener('onblur', vm.leaving);
  },
  

  beforeRouteEnter: function(to, from, next) {
    if (to.params.proposal_id) {
      let vm = this;
      Vue.http.get(`/api/proposal/${to.params.proposal_id}.json`).then(res => {
          next(vm => {
            vm.loading.push('fetching proposal')
            vm.proposal = res.body;
            //used in activities_land for T Class licence
            vm.proposal.selected_trails_activities=[];
            vm.proposal.selected_parks_activities=[];
            vm.proposal.marine_parks_activities=[];
            vm.loading.splice('fetching proposal', 1);
            vm.setdata(vm.proposal.readonly);
            vm.fetchProposalParks(to.params.proposal_id);
            // Vue.http.get(helpers.add_endpoint_json(api_endpoints.proposals,to.params.proposal_id+'/parks_and_trails')).then(response => {
            //     vm.parks = helpers.copyObject(response.body);
            //     console.log(vm.parks)
            // },
            //   error => {
            // });
            
            Vue.http.get(helpers.add_endpoint_json(api_endpoints.proposals,to.params.proposal_id+'/amendment_request')).then((res) => {
                     
                      vm.setAmendmentData(res.body);
                  
                },
              err => { 
                        console.log(err);
                  });
              });
          },
        err => {
          console.log(err);
        });    
    }
    else {
      Vue.http.post('/api/proposal.json').then(res => {
          next(vm => {
            vm.loading.push('fetching proposal')
            vm.proposal = res.body;
            vm.loading.splice('fetching proposal', 1);
          });
        },
        err => {
          console.log(err);
        });
    }
  }
}
</script>

<style lang="css" scoped>
</style>
