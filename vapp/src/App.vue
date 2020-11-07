<template>
  <div v-if="isDrizzleInitialized" id="app">
    <div class="logo">
      🦍 🧮
    </div>

    <!-- <div class="section">
      <drizzle-account units="Ether" :precision="2" />
    </div> -->

    <div class="section">
      <veCurveVault />
    </div>

  </div>

  <div v-else>Loading...</div>
</template>

<script>
import veCurveVault from './veCurveVault'
import { mapGetters } from 'vuex'

export default {
  name: 'app',
  components: {
    veCurveVault,
  },

  computed: mapGetters('drizzle', ['isDrizzleInitialized'])
}
</script>

<style>
#app {
  font-family: Menlo, Consolas, monospace;
  max-width: 600px;
  margin: auto;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
  margin-top: 60px;
}

.logo {
  font-size: 32px;
  margin-bottom: .8em;
  font-family: sans-serif;
}

h2 {
  font-weight: normal;
}
</style>
