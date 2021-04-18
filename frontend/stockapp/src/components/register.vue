<template src="@/assets/register/template.html"></template>
<style scoped src="@/assets/css/register.css"></style>
<script>
  import {register,login} from '@/apis/users.js'

  export default({
    name:'register',
    data(){
      return {
        agreecheck:false,
        usernameErrorMsg:'',
        passwordErrorMsg:'',
        emailErrorMsg:'',
        phoneErrorMsg:'',
        agreementErrorMsg:'',
        addressErrorMsg:'',
        isValid:true,
        isLogin:false,
        username:''
      }
    },
    mounted(){
      this.isLogin = window.localStorage.getItem("username") != null & window.localStorage.getItem("token") != null
      this.username = window.localStorage.getItem("username")
    },
    methods: {
      toSearch(){
        let stockno = document.getElementById('stockno').value
        if(!stockno){return}
          window.location.href = `/stockapp/#/stock/${stockno}`
      },
      logout(){
        window.localStorage.removeItem("token")
        window.localStorage.removeItem("username")
        window.location.reload()
      },
      register(){
        this.isValid = true
        this.usernameErrorMsg = this.passwordErrorMsg = this.emailErrorMsg = this.phoneErrorMsg = this.addressErrorMsg = this.agreementErrorMsg = ''
        let username = document.getElementById('username').value
        let pwd1 = document.getElementById('pwd1').value
        let pwd2 = document.getElementById('pwd2').value
        let email = document.getElementById('email').value
        let phone = document.getElementById('phone').value
        let address = document.getElementById('address').value
        if(!username){
          this.usernameErrorMsg = "用戶名稱不可空白"
          this.isValid = false
        }
        if(!pwd1 || !pwd2){
          this.passwordErrorMsg = "密碼不可空白"
          this.isValid = false
        }
        if(!email){
          this.emailErrorMsg = "E-mail不可空白"
          this.isValid = false
        }
        if(!phone){
          this.phoneErrorMsg = "電話不可空白"
          this.isValid = false
        }
        if(!address){
          this.addressErrorMsg = "地址不可空白"
          this.isValid = false
        }
        if(!this.agreecheck){
          this.agreementErrorMsg = "請勾選同意"
          this.isValid = false
        }
        let UsernameValidation = /[!@#$%^&*()\-_+=|\\{}[]"'\/.,]/
        let emailValidation =  /^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/
        if(UsernameValidation.test(username)){
          this.usernameErrorMsg = "使用者名稱不可包含特殊字元"
          return
        }
        if(pwd1 != pwd2){
          this.passwordErrorMsg = "密碼不一致"
          this.isValid = false
        }
        if(!emailValidation.test(email)){
          this.emailErrorMsg = "E-mail格式不合法"
          this.isValid = false
        }
        if(phone.length != 10){
          this.phoneErrorMsg = "電話格式不正確"
          this.isValid = false
        }
        if(!this.agreecheck){
          this.agreementErrorMsg = "請勾選同意"
          this.isValid = false
        }
        if(!this.isValid){
          return
        }
        let data = {
          'username':username,
          'password':pwd1,
          'email':email,
          'phone':phone,
          'address':address,
        }
        register(data).then(
          (response) => {
            if(response.data.status == 200){
              login(response.data.data).then(
                (response) => {
                  if(response.data.status == 200){
                    window.localStorage.setItem("username",response.data.data.username)
                    window.localStorage.setItem("token",response.data.data.token)
                    window.location.href = "/stockapp"
                  }
                  else{
                    alert(response.data.error)
                  }
                }
              )
            }
            else{
              alert(response.data.error)
            }
          }
        )
      }
    },
  })
</script>
