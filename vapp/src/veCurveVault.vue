<template lang="pug">
  div(v-if="isDrizzleInitialized")
    div
      p 🦍 user
      p crv balance: {{ crv_balance | fromWei }}
    div
      p 🧮 vault
      p total supply: {{ totalSupply | fromWei }}
</template>

<script>
import { mapGetters } from 'vuex'
import Web3 from 'web3'
let web3 = new Web3(Web3.givenProvider);

export default {
  name: 'veCurveVault',
  filters: {
    fromWei(data) {
      return data === 'loading' ? data : web3.utils.fromWei(data, 'ether')
    }
  },
  computed: {
    ...mapGetters('accounts', ['activeAccount', 'activeBalance']),
    ...mapGetters('drizzle', ['isDrizzleInitialized']),
    ...mapGetters('contracts', ['getContractData', 'contractInstances']),

    accounts() {
      return [this.activeAccount]
    },

    totalSupply() {
      return this.getContractData({contract: 'veCurveVault', method: 'totalSupply'})
    },

    crv_balance() {
      return this.getContractData({contract: 'CRV', method: 'balanceOf', methodArgs: [this.activeAccount]})
    },

    placeholders() {
      return ['To Address', 'Amount to Send']
    }
  },
  created() {
    this.$store.dispatch('drizzle/REGISTER_CONTRACT', {
      contractName: 'veCurveVault',
      method: 'totalSupply',
      methodArgs: [],
    }),
    this.$store.dispatch('drizzle/REGISTER_CONTRACT', {
      contractName: 'CRV',
      method: 'balanceOf',
      methodArgs: [this.activeAccount],
    })
  }
}
</script>

<style></style>
