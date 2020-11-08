<template lang="pug">
  div(v-if="isDrizzleInitialized")
    p
      h2 veCRV "Backscratcher" Vault
      p This vault accepts CRV in exchange for perpetual claim on Curve DAO admin fees across all Yearn products.
      p Since it locks CRV in Curve Voting Escrow for 4 years and regularly prolongs the lock, this vault doesn't have withdrawal functionality.
      p <strong>You will NOT get your CRV back. Ever.</strong>
    p
      div 🦍 user
      div wallet balance: {{ crv_balance | fromWei(2) }} CRV
      div vested balance: {{ vested_balance | fromWei(2) }} CRV
      div vault balance: {{ vault_balance | fromWei(2) }} yveCRV
      div claimable: {{ claimable | fromWei(2) }} 3pool
      //- div allowance: {{ crv_allowance | fromWei(2) }} CRV
    p
      div 🧮 vault
      div vault vs solo: {{ (yearn_vecrv / vault_supply).toFixed(3) }}x
      div total supply: {{ vault_supply | fromWei(2) }} yveCRV ({{ vault_supply / total_vecrv | toPct(3) }} of total)
      div yearn vecrv: {{ yearn_vecrv | fromWei(2) }} veCRV ({{ yearn_vecrv / total_vecrv | toPct(3) }} of total)
      div total vecrv: {{ total_vecrv | fromWei(2) }} veCRV
    p.row
      button(:disabled='has_allowance_vault', @click.prevent='on_approve_vault') {{ has_allowance_vault ? 'vault approved' : 'approve vault' }}
      button(:disabled='!has_allowance_vault', @click.prevent='on_deposit') deposit {{ crv_balance | fromWei(2) }} CRV
      button(@click.prevent='on_claim') claim {{ claimable | fromWei(2) }} rewards
    p.row
      button(:disabled='has_allowance_zap', @click.prevent='on_approve_zap') {{ has_allowance_zap ? 'zap approved' : 'approve zap' }}
      button(:disabled='!has_allowance_zap', @click.prevent='on_zap') zap {{ zap_balance | fromWei(2) }} CRV
</template>

<script>
import { mapGetters } from 'vuex'
import ethers from 'ethers'
const max_uint = new ethers.BigNumber.from(2).pow(256).sub(1).toString()

export default {
  name: 'veCurveVault',
  filters: {
    fromWei(data, precision) {
      if (data === 'loading') return data
      if (data > 2**255) return '∞'
      let value = ethers.utils.commify(ethers.utils.formatEther(data))
      let parts = value.split('.')
      return parts[0] + '.' + parts[1].slice(0, precision)
    },
    toPct(data, precision) {
      if (isNaN(data)) return '?'
      return `${(data * 100).toFixed(precision)}%`
    }
  },
  methods: {
    on_approve_vault() {
      this.drizzleInstance.contracts['CRV'].methods['approve'].cacheSend(this.vault, max_uint, {from: this.activeAccount})
    },
    on_approve_zap() {
      this.drizzleInstance.contracts['CRV'].methods['approve'].cacheSend(this.zap, max_uint, {from: this.activeAccount})
    },
    on_deposit() {
      this.drizzleInstance.contracts['veCurveVault'].methods['depositAll'].cacheSend({from: this.activeAccount})
    },
    on_zap() {
      this.drizzleInstance.contracts['CurveVestingBackscratch'].methods['zap'].cacheSend({from: this.activeAccount})
    },
    on_claim() {
      this.drizzleInstance.contracts['veCurveVault'].methods['claim'].cacheSend({from: this.activeAccount})
    },
    call(contract, method, args) {
      let key = this.drizzleInstance.contracts[contract].methods[method].cacheCall(...args)
      try {
        return new ethers.BigNumber.from(this.contractInstances[contract][method][key].value)
      } catch (error) {
        return new ethers.BigNumber.from(0)
      }
    },
  },
  computed: {
    ...mapGetters('accounts', ['activeAccount', 'activeBalance']),
    ...mapGetters('drizzle', ['drizzleInstance', 'isDrizzleInitialized']),
    ...mapGetters('contracts', ['getContractData', 'contractInstances']),

    user() {
      return this.activeAccount
    },
    vault() {
      return this.drizzleInstance.contracts['veCurveVault'].address
    },
    zap() {
      return this.drizzleInstance.contracts['CurveVestingBackscratch'].address
    },
    voter() {
      return this.drizzleInstance.contracts['CurveYCRVVoter'].address
    },
    vault_supply() {
      return this.call('veCurveVault', 'totalSupply', [])
    },
    crv_balance() {
      return this.call('CRV', 'balanceOf', [this.activeAccount])
    },
    vested_balance() {
      return this.call('CurveVesting', 'balanceOf', [this.activeAccount])
    },
    zap_balance() {
      return this.crv_balance.add(this.vested_balance)
    },
    crv_allowance() {
      return this.call('CRV', 'allowance', [this.activeAccount, this.vault])
    },
    vault_balance() {
      return this.call('veCurveVault', 'balanceOf', [this.activeAccount])
    },
    claimable() {
      return this.call('veCurveVault', 'claimable', [this.activeAccount])
    },
    yearn_vecrv() {
      return this.call('CurveVotingEscrow', 'balanceOf', [this.voter])
    },
    total_vecrv() {
      return this.call('CurveVotingEscrow', 'totalSupply', [])
    },
    has_allowance_vault() {
      return !this.call('CRV', 'allowance', [this.activeAccount, this.vault]).isZero()
    },
    has_allowance_zap() {
      return !this.call('CRV', 'allowance', [this.activeAccount, this.zap]).isZero()
    },
  },
}
</script>

<style>
.row > button {
  margin-right: 1em;
}
</style>
