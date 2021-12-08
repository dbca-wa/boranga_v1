var site_url = location.origin
var t_class='Commercial operations'
var filming='Filming'
var event='Event'

module.exports = {
    organisations: '/api/organisations.json',
    filtered_organisations: '/api/filtered_organisations',
    organisation_requests: '/api/organisation_requests.json',
    organisation_contacts: '/api/organisation_contacts.json',
    organisation_access_group_members: '/api/organisation_access_group_members',
    users: '/api/users.json',
    profile: '/api/profile',
    department_users: '/api/department_users',
    filtered_users: '/api/filtered_users',
    referral_recipient_groups: '/api/referrals/user_group_list',
    //other
    //countries: "https://restcountries.eu/rest/v1/?fullText=true",
    countries: '/api/countries',
    proposal_type:"/api/proposal_type",
    proposals:"/api/proposal.json",
    proposal_park:"/api/proposal_park.json",
    proposal_submit:"/api/proposal_submit.json",
    //list_proposals:"/api/proposal/list_proposal.json",
    approvals:"/api/approvals.json",
    referrals:"/api/referrals.json",
    compliances:"/api/compliances.json",
    proposal_standard_requirements:"/api/proposal_standard_requirements.json",
    proposal_requirements:"/api/proposal_requirements.json",
    amendment_request:"/api/amendment_request.json",
    regions:"/api/regions.json",
    park_treeview:"/api/park_treeview",
    marine_treeview:"/api/marine_treeview",
    tclass_container_land:"/api/tclass_container_land",
    tclass_container_marine:"/api/tclass_container_marine",
    activity_matrix:"/api/activity_matrix.json",
    application_types:"/api/application_types.json",
    access_types:"/api/access_types.json",
    parks:"/api/parks.json",
    trails:"/api/trails.json",
    districts:"/api/districts.json",
    vehicles:"/api/vehicles.json",
    vessels:"/api/vessels.json",
    assessments:"/api/assessments.json",
    event_trail_container:"/api/event_trail_container",
    event_park_container:"/api/event_park_container",
    overdue_invoices:"/api/overdue_invoices.json",
    
    //filming
    proposal_filming_parks:"/api/proposal_filming_parks.json",
    district_proposals:"/api/district_proposals.json",

    //Events
    proposal_events_parks:"/api/proposal_events_parks.json",
    abseiling_climbing_activities:"/api/abseiling_climbing_activities.json",
    proposal_pre_event_parks:"/api/proposal_pre_event_parks.json",
    proposal_events_trails:"/api/proposal_events_trails.json",

    // used in internal and external dashboards
    proposals_paginated_external:   "/api/proposal_paginated/proposals_external/?format=datatables",
    approvals_paginated_external:   "/api/approval_paginated/approvals_external/?format=datatables",
    compliances_paginated_external: "/api/compliance_paginated/compliances_external/?format=datatables",
    proposals_paginated_internal:   "/api/proposal_paginated/proposals_internal/?format=datatables",
    referrals_paginated_internal:   "/api/proposal_paginated/referrals_internal/?format=datatables",
    species_communities_paginated_internal: "/api/proposal_paginated/species_communities_internal/?format=datatables",

    //filter_list:                    "/api/proposal_paginated/filter_list.json",
    filter_list:                    "/api/proposal/filter_list.json",
    filter_list_approvals:          "/api/approvals/filter_list.json",
    filter_list_compliances:        "/api/compliances/filter_list.json",
    filter_list_referrals:          "/api/referrals/filter_list.json",
    filter_list_parks:              "/api/parks/filter_list.json",
    filter_list_district_proposals:  "/api/district_proposals/filter_list.json",

    //approvals_paginated:"/api/approvals/user_list_paginated/?format=datatables",
    //compliances_paginated:"/api/compliances/user_list_paginated/?format=datatables",
    //list_proposals:"/api/list_proposal/?format=datatables",
    //list_referrals:"/api/list_proposal/referral_list/?format=datatables",

    discard_proposal:function (id) {
      return `/api/proposal/${id}.json`;
    },
    discard_vessel:function (id) {
      return `/api/vessels/${id}.json`;
    },
    discard_vehicle:function (id) {
      return `/api/vehicles/${id}.json`;
    },
    discard_abseiling_climbing:function (id) {
      return `/api/abseiling_climbing_activities/${id}.json`;
    },
    discard_pre_event_park:function (id) {
      return `/api/proposal_pre_event_parks/${id}.json`;
    },
    discard_event_park:function (id) {
      return `/api/proposal_events_parks/${id}.json`;
    },
    discard_event_trail:function (id) {
      return `/api/proposal_events_trails/${id}.json`;
    },
    discard_filming_park:function (id) {
      return `/api/proposal_filming_parks/${id}.json`;
    },
    site_url: site_url,
    //dep_name: 'Department of Biodiversity, Conservation and Attractions',
    //dep_name_short: 'DBCA',
    system_name: 'Boranga System',
    //system_name_short: 'DAS',
    payment_help_url: 'https://parks.dpaw.wa.gov.au/for-business/training-accreditation-insurance-fees',
    proposal_type_help_url: ' https://parks.dbca.wa.gov.au/for-business/commercial-operations-licensing',
    t_class: t_class,
    filming: filming,
    event: event,
    group_types:['Fauna', 'Flora', 'Communities']
}
