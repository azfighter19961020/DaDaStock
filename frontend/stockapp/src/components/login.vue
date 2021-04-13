<template src="@/assets/login/template.html"></template>
<style scoped src="@/assets/css/login.css"></style>
<script>
  import {login} from '@/apis/users.js'
  export default({
    name:'login',
    data(){
      return {
        usernameErrMsg:'',
        passwordErrMsg:'',
        isLogin:false,
        username:''
      }
    },
    mounted(){
      this.isLogin = window.localStorage.getItem("username") != null & window.localStorage.getItem("token") != null
      this.username = window.localStorage.getItem("username")
    },
    methods:{
      toSearch(){
        let stockno = document.getElementById('stockno').value
        if(!stockno){return}
          window.location.href = `http://localhost:8080/#/stock/${stockno}`
      },
      flogin(){
        this.usernameErrMsg = this.passwordErrMsg = ''
        let username = document.getElementById('username').value
        let password = document.getElementById('pwd').value
        if(!username){
          this.usernameErrMsg = "用戶名不可空白"
        }
        if(!password){
          this.passwordErrMsg = "密碼不可空白"
        }
        if(!username || !password){
          return
        }
        let data = {
          'username':username,
          'password':password
        }
        login(data).then(
          (response) => {
            if(response.data.status == 200){
              window.localStorage.setItem('username',response.data.data.username)
              window.localStorage.setItem('token',response.data.data.token)
              this.isLogin = true
              this.username = response.data.data.username
              window.location.href = '/'
            }
            else{
              alert(response.data.error)
            }
          }
        )

      },
      logout(){
        window.localStorage.removeItem("token")
        window.localStorage.removeItem("username")
        window.location.reload()
      },
    },
  })
</script>