<template lang="pug">
  div(v-if="isDrizzleInitialized")
    p
      h2 veCRV "Backscratcher" Vault
      p This vault accepts CRV in exchange for perpetual claim on Curve DAO admin fees across all Yearn products.
      p Since it locks CRV in Curve Voting Escrow for 4 years and regularly prolongs the lock, this vault doesn't have withdrawal functionality.
      p <strong>You will NOT get your CRV back. Ever.</strong>
    p
      div 🦍 user
      div token balance: {{ crv_balance | fromWei }} CRV
      div vault balance: {{ vault_balance | fromWei }} yveCRV
      div claimable: {{ claimable | fromWei }} 3pool
      //- div allowance: {{ crv_allowance | fromWei }} CRV
    p
      div 🧮 vault
      div total supply: {{ totalSupply | fromWei }} yveCRV ({{ totalSupply / total_vecrv | toPct }} of total)
      div yearn vecrv: {{ yearn_vecrv | fromWei }} veCRV ({{ yearn_vecrv / total_vecrv | toPct }} of total)
      div total vecrv: {{ total_vecrv | fromWei }} veCRV
    p.row
      button(:disabled='has_allowance', @click.prevent='on_approve') {{ has_allowance ? 'approved' : 'approve vault' }}
      button(:disabled='!has_allowance', @click.prevent='on_deposit') deposit {{ crv_balance | fromWei }} CRV
      button(@click.prevent='on_claim') claim {{ claimable | fromWei }} rewards
</template>

<script>
import { mapGetters } from 'vuex'
import Web3 from 'web3'
import ethers from 'ethers'

let web3 = new Web3(Web3.givenProvider);

export default {
  name: 'veCurveVault',
  filters: {
    fromWei(data) {
      if (data === 'loading') return data
      if (data > 2**255) return '∞'
      let value = ethers.utils.commify(ethers.utils.formatEther(data))
      let parts = value.split('.')
      return parts[0] + '.' + parts[1].slice(0, 2)
    },
    toPct(data) {
      if (isNaN(data)) return '?'
      return `${(data * 100).toFixed(2)}%`
    }
  },
  methods: {
    on_approve() {
      let max_uint = new ethers.BigNumber.from(2).pow(256).sub(1).toString()
      let args = [this.drizzleInstance.contracts['veCurveVault'].address, max_uint, {from: this.activeAccount}]
      this.drizzleInstance.contracts['CRV'].methods['approve'].cacheSend(...args)
    },
    on_deposit() {
      this.drizzleInstance.contracts['veCurveVault'].methods['depositAll'].cacheSend({from: this.activeAccount})
    },
    on_claim() {
      this.drizzleInstance.contracts['veCurveVault'].methods['claim'].cacheSend({from: this.activeAccount})
    },
  },
  computed: {
    ...mapGetters('accounts', ['activeAccount', 'activeBalance']),
    ...mapGetters('drizzle', ['drizzleInstance', 'isDrizzleInitialized']),
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
    crv_allowance() {
      return this.getContractData({contract: 'CRV', method: 'allowance', methodArgs: [this.activeAccount, this.drizzleInstance.contracts['veCurveVault'].address]})
    },
    vault_balance() {
      return this.getContractData({contract: 'veCurveVault', method: 'balanceOf', methodArgs: [this.activeAccount]})
    },
    claimable() {
      return this.getContractData({contract: 'veCurveVault', method: 'claimable', methodArgs: [this.activeAccount]})
    },
    yearn_vecrv() {
      return this.getContractData({contract: 'CurveVotingEscrow', method: 'balanceOf', methodArgs: [this.drizzleInstance.contracts['CurveYCRVVoter'].address]})
    },
    total_vecrv() {
      return this.getContractData({contract: 'CurveVotingEscrow', method: 'totalSupply'})
    },
    has_allowance() {
      let allowance = this.getContractData({contract: 'CRV', method: 'allowance', methodArgs: [this.activeAccount, this.drizzleInstance.contracts['veCurveVault'].address]})
      let balance = this.getContractData({contract: 'CRV', method: 'balanceOf', methodArgs: [this.activeAccount]})
      if (isNaN(allowance) || isNaN(balance)) return
      return new ethers.BigNumber.from(allowance).gt(new ethers.BigNumber.from(balance))
    },
  },
  created() {
    this.$store.dispatch('drizzle/REGISTER_CONTRACT', {contractName: 'veCurveVault', method: 'totalSupply', methodArgs: []}),
    this.$store.dispatch('drizzle/REGISTER_CONTRACT', {contractName: 'CRV', method: 'balanceOf', methodArgs: [this.activeAccount]})
    this.$store.dispatch('drizzle/REGISTER_CONTRACT', {contractName: 'CRV', method: 'allowance', methodArgs: [this.activeAccount, this.drizzleInstance.contracts['veCurveVault'].address]})
    this.$store.dispatch('drizzle/REGISTER_CONTRACT', {contractName: 'veCurveVault', method: 'balanceOf', methodArgs: [this.activeAccount]})
    this.$store.dispatch('drizzle/REGISTER_CONTRACT', {contractName: 'veCurveVault', method: 'claimable', methodArgs: [this.activeAccount]})
    this.$store.dispatch('drizzle/REGISTER_CONTRACT', {contractName: 'CurveVotingEscrow', method: 'balanceOf', methodArgs: [this.drizzleInstance.contracts['CurveYCRVVoter'].address]})
    this.$store.dispatch('drizzle/REGISTER_CONTRACT', {contractName: 'CurveVotingEscrow', method: 'totalSupply', methodArgs: []})
  }
}
</script>

<style>
.row > button {
  margin-right: 1em;
}
</style>
