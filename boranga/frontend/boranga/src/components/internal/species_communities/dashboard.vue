<template>
<div class="container" id="internalDash">
    <SpeciesCommunitiesDashTable level="internal" :url="species_communities_url"/>
</div>
</template>
<script>
import SpeciesCommunitiesDashTable from '@common-utils/species_communities_dashboard.vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
    name: 'InternalSpeciesCommunitiesDashboard',
    data() {
        let vm = this;
        return {
            //approvals_url: api_endpoints.approvals_paginated_external,
            species_communities_url: api_endpoints.species_communities_paginated_internal,
        }
    
    },
    watch: {},
    components: {
        SpeciesCommunitiesDashTable,
    },
    computed: {
    },
    methods: {},
    mounted: function () {
    }
}
</script>
