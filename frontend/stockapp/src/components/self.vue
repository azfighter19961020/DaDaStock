<template src="@/assets/self/template.html"></template>
<style scoped src="@/assets/css/self.css"></style>
<script>
  import {getUserData,fixUserData,storeBalance} from '@/apis/users.js'
  import eye_close from '@/assets/images/eye_close.png'
  import eye_open from '@/assets/images/eye_open.png'
  import {getOrder,cancelOrder} from '@/apis/order.js'
  import {getInventory} from '@/apis/inventory.js'
  import {LetterCube} from 'vue-loading-spinner'
  export default({
    name:'self',
    components: {
      LetterCube
    },
    data(){
      return {
        isLogin:false,
        username:'',
        eyeId: false,
        eyeToken: false,
        eyeBalance:false,
        secretToken:'',
        secretClientId:'',
        orderdata:null,
        balance:0,
        inventoryData:null,
        userdata:null,
        isLoading: false,
        storeText:'',
        isStore:false,
      }
    },
    methods:{
      logout(){
        window.localStorage.removeItem("username")
        window.localStorage.removeItem("token")
        window.location.href = '/stockapp/#/login'
      },
      toSearch(){
        let stockno = document.getElementById('stockno').value
        if(!stockno){return}
          window.location.href = `/stockapp/#/stock/${stockno}`
      },
      toStore(){
        if(this.storeText == ""){
          alert("儲值金額不為空!")
          return
        }
        if(parseInt(this.storeText) > Math.pow(10,5)){
          alert("金額超出限制!請勿超過100000!")
          this.storeText = ""
          return
        }
        let token = window.localStorage.getItem("token")
        let username = window.localStorage.getItem("username")
        let data = {
          "username":username,
          "storeBalance":this.storeText
        }
        storeBalance(token,data).then(
          (response) => {
            if(response.data.status == 200){
              alert("儲值成功!")
              window.location.reload()
            }
            else{
              alert(response.data.error)
            }
          }
        )
      },
      showStoreMain(){
        this.isStore = !this.isStore
      },
      cancelOrderFunc(orderno){
        let data = {
          "secretToken":this.secretToken,
          "secretClientId":this.secretClientId,
          "orderno":orderno
        }
        cancelOrder(data).then(
           (response) => {
            if(response.data.status == 200){
              window.location.reload()
            }
            else{
              alert(response.data.message)
            }
           }
        )
      },
      fixPassword(){
        let oldpassword = document.getElementById("oldPassword").value
        let newpassword = document.getElementById("newPassword").value
        let username = window.localStorage.getItem("username")
        let token = window.localStorage.getItem("token")
        if(oldpassword == "" || newpassword == ""){
          alert("輸入不完整!")
          return
        }
        let data = {
          "fixType":"password",
          "fixValue":"",
          "newpassword":newpassword,
          "oldpassword":oldpassword,
          "username":username,
        }
        fixUserData(token,data).then(
          (response) => {
            if(response.data.status == 200){
              alert("修改成功!")
              window.location.reload()
            }
            else{
              alert(response.data.error)
            }
          }
        )
      },
      fix(fixType){
        let fixValue = document.getElementById(fixType).value
        if(fixValue == null){
          return
        }
        let username = window.localStorage.getItem("username")
        let token = window.localStorage.getItem("token")
        if(!username || !token){
          alert("請重新登入!")
          return
        }
        let data = {
          "username":username,
          "fixType":fixType,
          "fixValue":fixValue
        }
        fixUserData(token,data).then(
          (response) => {
            if(response.data.status == 200){
              window.location.reload()
            }
            else{
              alert(response.data.error)
            }
          }
        )
      },
      IdFade(){
        let eye = document.getElementById("eyeId")
        let secretClientId = document.getElementById("secretClientId")
        if(this.eyeId){
          eye.src = eye_close
          secretClientId.value = "*".repeat(this.secretClientId.length)
        }
        else{
          eye.src = eye_open
          secretClientId.value = this.secretClientId
        }
        this.eyeId = !this.eyeId
      },
      balanceFade(){
        let eye = document.getElementById("eyeBalance")
        let balance = document.getElementById("balance")
        if(this.eyeBalance){
          eye.src = eye_close
          balance.value = "*".repeat(this.balance.toString().length)
        }
        else{
          eye.src = eye_open
          balance.value = this.balance.toLocaleString()
        }
        this.eyeBalance = !this.eyeBalance
      },
      tokenFade(){
        let eye = document.getElementById("eyeToken")
        let secretToken = document.getElementById("secretToken")
        if(this.eyeToken){
          eye.src = eye_close
          secretToken.value = "*".repeat(this.secretToken.length)
        }
        else{
          eye.src = eye_open
          secretToken.value = this.secretToken
        }
        this.eyeToken = !this.eyeToken
      }
    },
    async mounted(){
     this.isLoading = true
     this.isLogin = window.localStorage.getItem("username") != null & window.localStorage.getItem("token") != null
      if(!this.isLogin){
        alert("請登入!")
        window.location.href = "/#/login"
      }
      let username = window.localStorage.getItem("username")
      this.username = username
      let token = window.localStorage.getItem("token")
      let data = {"username":username}
      let [ruserdata,rorderdata,rinventorydata] = await Promise.all([getUserData(username,token),getOrder(data,token),getInventory(token,data)])
      let userdata = ruserdata.data.data
      let orderdata = rorderdata.data.data
      let inventoryData = rinventorydata.data.data
      this.userdata = userdata
      this.orderdata = orderdata
      this.inventoryData = inventoryData
      this.secretClientId = userdata.secretClientId
      this.secretToken = userdata.secretToken
      this.balance = userdata.balance
      let user = document.getElementById("username")
      let email = document.getElementById("email")
      let phone = document.getElementById("phone")
      let address = document.getElementById("address")
      let secretClientId = document.getElementById("secretClientId")
      let secretToken = document.getElementById("secretToken")
      let balance = document.getElementById("balance")
      user.value = this.userdata.username
      email.value = this.userdata.email
      phone.value = this.userdata.phone
      address.value = this.userdata.address
      balance.value = "*".repeat(this.balance.toString().length)
      secretClientId.value = "*".repeat(this.secretClientId.length)
      secretToken.value = "*".repeat(this.secretToken.length)
      this.isLoading = false
    },
  })
</script>
