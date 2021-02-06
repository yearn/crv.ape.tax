<template lang="pug">
  div(v-if="isDrizzleInitialized", id="app")
    .logo
    .section
      veCurveVault
  div(v-else)
    .container
      div 🦍 🧮
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
  font-family: Menlo, monospace;
  max-width: 600px;
  margin: auto;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
  margin-top: 60px;
}
.logo {
  width: 64px;
  height: 64px;
  display: block;
  background: url(assets/logo.svg);
  background-repeat: no-repeat;
  background-size: 64px;
}
h2 {
  font-weight: normal;
}
.container {
  display: flex;
  position: absolute;
  height: 100%;
  width: 100%;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.container > div {
  font-size: 36px;
}
</style>
