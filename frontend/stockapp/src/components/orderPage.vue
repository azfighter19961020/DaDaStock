<template src="@/assets/orderPage/template.html"></template>
<style scoped src="@/assets/css/order.css"></style>
<script>
  import {createOrder} from '@/apis/order.js'
  import {getClosePriceNear} from '@/apis/stock.js'
  import {LetterCube} from 'vue-loading-spinner'
  export default{
    name:'orderPage',
    data(){
      return {
        isLogin:false,
        username:'',
        stockno:'',
        tradeType:'',
        tradeCategory:'',
        orderType:'',
        takeprice:'',
        closepriceNear:'',
        LimitDown:0,
        LimitUp:0,
        Unchanged:0,
        pendingType:'',
        stockname:'',
        primaryTradeType:'',
        isLoading:false,
        inputStockno:'',
        timer:null,
        overtime:false,
        overtimeMsg:'',
        priceErrorMsg:'',
        userprice:''
      }
    },
    components: {
        LetterCube
    },
    mounted(){
      // terminated trade time : 13:30
      // this.clockTime = new Date(Date.now()).getHours()
      this.timer = setInterval(this.detectTime,1000)
      this.isLoading = true
      this.isLogin = window.localStorage.getItem("username") != null & window.localStorage.getItem("token") != null
      this.username = window.localStorage.getItem("username")
      if(this.$route.params.stockno != null){
        this.stockno = this.$route.params.stockno
        this.inputStockno = this.$route.params.stockno
        getClosePriceNear(this.stockno).then(
          (response) => {
            if(response.data.status == 200){
              this.closepriceNear = response.data.data.closeprice
              // this.LimitDown = this.closepriceNear * 0.9
              // this.LimitUp = this.closepriceNear * 1.1
              this.LimitDown = (response.data.data.limitDown).toFixed(2)
              this.LimitUp = (response.data.data.limitUp).toFixed(2)
              this.Unchanged = this.closepriceNear
              this.stockname = response.data.stockname
              let price = document.getElementById("price")
              price.value = (this.closepriceNear).toFixed(2)
              this.userprice = (this.closepriceNear).toFixed(2)
              this.takeprice = "Current"
              var elements = document.getElementsByClassName("takePriceButton")
              for(var i=0;i<elements.length;i++){
                if(elements[i].id == "Current"){
                  elements[i].className = "btn btn-primary takePriceButton"
                }
                else{
                  elements[i].className = "btn btn-outline-primary takePriceButton"
                }
              }
            }
            else{
              alert(response.data.error)
            }
            this.isLoading = false
          }
        )
      }else{
        this.isLoading = false
      }
    },
    watch: {
      inputStockno: {
        handler: function(){
        if(this.inputStockno.length != 4){
          return
        }
        this.isLoading = true
        getClosePriceNear(this.inputStockno).then(
          (response) => {
            if(response.data.status == 200){
              this.stockno = response.data.stockno
              this.closepriceNear = response.data.data.closeprice
              // this.LimitDown = (this.closepriceNear * 0.9).toFixed(2)
              // this.LimitUp = (this.closepriceNear * 1.1).toFixed(2)
              this.LimitDown = (response.data.data.limitDown).toFixed(2)
              this.LimitUp = (response.data.data.limitUp).toFixed(2)
              this.Unchanged = this.closepriceNear
              this.stockname = response.data.stockname
              let price = document.getElementById("price")
              price.value = (this.closepriceNear).toFixed(2)
              this.userprice = (this.closepriceNear).toFixed(2)
              this.takeprice = "Current"
              var elements = document.getElementsByClassName("takePriceButton")
              for(var i=0;i<elements.length;i++){
                if(elements[i].id == "Current"){
                  elements[i].className = "btn btn-primary takePriceButton"
                }
                else{
                  elements[i].className = "btn btn-outline-primary takePriceButton"
                }
              }
              this.isLoading = false
            }
            else{
              alert(response.data.error)
              this.isLoading = false
            }
          }
        )
        }
      },
      userprice: {
        handler: function(){
          let elements = document.getElementsByClassName("takePriceButton")
          var i = 0
          if((parseFloat(this.userprice) != parseFloat(this.LimitUp)) && (parseFloat(this.userprice) != parseFloat(this.LimitDown)) && (parseFloat(this.userprice) != parseFloat(this.closepriceNear))){
            this.takeprice = "Current"
            for(i=0;i<elements.length;i++){
              if(elements[i].id == "Current"){
                elements[i].className = "btn btn-primary takePriceButton"
              }
              else{
                elements[i].className = "btn btn-outline-primary takePriceButton"
              }
            }
          }
          else if(parseFloat(this.userprice) == parseFloat(this.LimitUp)){
            this.takeprice = "LimitUp"
            for(i=0;i<elements.length;i++){
              if(elements[i].id == "LimitUp"){
                elements[i].className = "btn btn-primary takePriceButton"
              }
              else{
                elements[i].className = "btn btn-outline-primary takePriceButton"
              }
            }          
          }
          else if(parseFloat(this.userprice) == parseFloat(this.LimitDown)){
            this.takeprice = "LimitDown"
            for(i=0;i<elements.length;i++){
              if(elements[i].id == "LimitDown"){
                elements[i].className = "btn btn-primary takePriceButton"
              }
              else{
                elements[i].className = "btn btn-outline-primary takePriceButton"
              }
            }
          }
          else if(parseFloat(this.userprice) == parseFloat(this.closepriceNear)){
            if(this.overtime){
              return
            }
            this.takeprice = "Unchanged"
            for(i=0;i<elements.length;i++){
              if(elements[i].id == "Unchanged"){
                elements[i].className = "btn btn-primary takePriceButton"
              }
              else{
                elements[i].className = "btn btn-outline-primary takePriceButton"
              }
            }
          }
        }
      }
    },
    destroyed(){
      clearInterval(this.timer)
    },
    methods:{
      detectTime(){
        let hour = new Date(Date.now()).getHours()
        if(hour >= 13 & hour < 18){
          this.overtime = true
          this.overtimeMsg = "已經超過交易時間，將只能選擇ROD，並且不可選擇現價"
          let takeprices = document.getElementsByClassName("takePriceButton")
          for(var i = 0; i < takeprices.length; i++){
            if(takeprices[i].id == 'Unchanged'){
              takeprices[i].className = "btn btn-outline-primary takePriceButton"
              takeprices[i].disabled = true
            }
          }
          let pendingTypes = document.getElementsByClassName("pendingTypeButton")
          this.pendingType = "ROD"
          for(i=0;i<pendingTypes.length;i++){
            if(pendingTypes[i].id != "ROD"){
              pendingTypes[i].className = "btn btn-outline-primary pendingTypeButton"
              pendingTypes[i].disabled = true
            }
          } 
          clearInterval(this.timer)
        }
      },
      toSearch(){
        let stockno = document.getElementById('stockno').value
        if(!stockno){return}
          window.location.href = `/stockapp/#/stock/${stockno}`
      },
      amountProcess(type){
        let amount = document.getElementById("amount")
        let value = parseInt(amount.value)
        if(type == '+'){value += 1}
        if(type == '-'){if(value == 1){return}else{value -= 1}}
        amount.value = value
      },
      priceProcess(type){
        let price = document.getElementById("price")
        let value = parseInt(price.value)
        if(type == '+'){value += 1}
        if(type == '-'){if(value == 1){return}else{value -= 1}}
        price.value = value
      },
      logout(){
        window.localStorage.removeItem("username")
        window.localStorage.removeItem("token")
        window.location.href = "/stockapp/#/login"
      },
      submitOrder(){
        let tradeType = this.tradeType
        let tradeCategory = this.tradeCategory
        let orderType = this.orderType
        let amount = document.getElementById("amount").value
        if(parseInt(amount) < 1){
          alert("數量請勿小於1!")
          return
        }
        if(this.tradeType == "Common" || this.tradeType == "Fixing"){
          if(parseInt(amount) % 1000 != 0){
            alert("選取整股，但數量不為1000的倍數!")
            return
          }
        }
        let price = this.userprice
        if(price > parseFloat(this.LimitUp) || price < parseFloat(this.LimitDown)){
          this.priceErrorMsg = "取價錯誤，漲跌幅不可超過±10%"
          return
        }
        else{
          this.priceErrorMsg = ""
        }
        let takeprice = this.takeprice
        let username = this.username
        let stockno = this.stockno
        let pendingType = this.pendingType
        let isAPI = false
        let data = {
          "tradeType":tradeType,
          "tradeCategory":tradeCategory,
          "orderType":orderType,
          "amount":amount,
          "price":price,
          "username":username,
          "stockno":stockno,
          "isAPI":isAPI,
          "takeprice":takeprice,
          "pendingType":pendingType,
        }
        createOrder(data).then(
          (response) => {
            if(response.data.status == 200){
              window.location.href = "/stockapp/#/self"
            }
            else{
              alert(response.data.error)
            }
          }
        )
      },
      changePendingType(param){
        this.pendingType = param
        let elements = document.getElementsByClassName("pendingTypeButton")
        for(var i=0;i<elements.length;i++){
          if(elements[i].id == param){
            elements[i].className = "btn btn-primary pendingTypeButton"
          }
          else{
            elements[i].className = "btn btn-outline-primary pendingTypeButton"
          }
        }
       
      },
      changePrimaryTradeType(param){
        let elements = document.getElementsByClassName("tradeTypeButton")
        for(var i=0;i<elements.length;i++){
          if(elements[i].id == param){
            elements[i].className = "btn btn-primary tradeTypeButton"
          }
          else{
            elements[i].className = "btn btn-outline-primary tradeTypeButton"
          }
        }
        this.primaryTradeType = param
        if(this.primaryTradeType == "Intraday" && this.tradeType != "Odd" && this.tradeType != "IntradayOdd"){
          let elements = document.getElementsByClassName("tradeCategoryButton")
          for(i=0;i<elements.length;i++){
            if(elements[i].className.split(" ")[1] != "btn-primary"){
              elements[i].className = "btn btn-outline-primary tradeCategoryButton"
              elements[i].disabled = false
            }
          }
        }
      },
      changeTradeType(param){
        if(this.primaryTradeType == "Intraday"){
          if(param == "Common"){
            this.tradeType = "Common"
          }
          else if(param == "Odd"){
            this.tradeType = "IntradayOdd"
          }
        }
        else if(this.primaryTradeType == "Out"){
          if(param == "Common"){
            this.tradeType = "Fixing"
          }
          else if(param == "Odd"){
            this.tradeType = "Odd"
          }
        }
        let elements = document.getElementsByClassName("tradeTypeSecondButton")
        for(var i=0;i<elements.length;i++){
          if(elements[i].id == param){
            elements[i].className = "btn btn-primary tradeTypeSecondButton"
          }
          else{
            elements[i].className = "btn btn-outline-primary tradeTypeSecondButton"
          }
        }
        if(this.primaryTradeType == "Out" || this.tradeType == "IntradayOdd"){
          if(!this.overtime){
            let takeprices = document.getElementsByClassName("takePriceButton")
            this.takeprice = "Unchanged"
            for(i = 0; i < takeprices.length; i++){
              if(takeprices[i].id != 'Unchanged'){
                takeprices[i].className = "btn btn-outline-primary takePriceButton"
                takeprices[i].disabled = true
              }
              else{
               takeprices[i].className = "btn btn-primary takePriceButton"
              }
            }            
          }
          let tradeCategorys = document.getElementsByClassName("tradeCategoryButton")
          this.tradeCategory = "Cash"
          for(i=0;i<tradeCategorys.length;i++){
            if(tradeCategorys[i].id != 'Cash'){
              tradeCategorys[i].className = "btn btn-outline-primary tradeCategoryButton"
              tradeCategorys[i].disabled = true
            }
            else{
              tradeCategorys[i].className = "btn btn-primary tradeCategoryButton"
            }
          }
          let pendingTypes = document.getElementsByClassName("pendingTypeButton")
          this.pendingType = "ROD"
          for(i=0;i<pendingTypes.length;i++){
            if(pendingTypes[i].id != "ROD"){
              pendingTypes[i].className = "btn btn-outline-primary pendingTypeButton"
              pendingTypes[i].disabled = true
            }
            else{
              pendingTypes[i].className = "btn btn-primary pendingTypeButton"
            }
          }
          if(!this.overtime){
            let price = document.getElementById("price")
            price.value = this.Unchanged            
          }
        }
        if(param == "Odd"){
          let amount = document.getElementById("amount")
          amount.value = 1
        }
        else if(this.primaryTradeType != "Out"){
          if(!this.overtime){
            let takeprices = document.getElementsByClassName("takePriceButton")
            for(i = 0; i < takeprices.length;i++){
              if(takeprices[i].className.split(" ")[1] != "btn-primary"){
                takeprices[i].className = "btn btn-outline-primary takePriceButton"
                takeprices[i].disabled = false
              }
            }           
          }
          let amount = document.getElementById("amount")
          amount.value = 1000
          let tradeCategorys = document.getElementsByClassName("tradeCategoryButton")
          for(i=0;i<tradeCategorys.length;i++){
            if(tradeCategorys[i].className.split(" ")[1] != "btn-primary"){
              tradeCategorys[i].className = "btn btn-outline-primary tradeCategoryButton"
              tradeCategorys[i].disabled = false
            }
          }
          if(!this.overtime){
            let pendingTypes = document.getElementsByClassName("pendingTypeButton")
            for(i=0;i<pendingTypes.length;i++){
              if(pendingTypes[i].className.split(" ")[1] != "btn-primary"){
                pendingTypes[i].className = "btn btn-outline-primary pendingTypeButton"
                pendingTypes[i].disabled = false
              }
            }            
          }
        }
      },
      changeTradeCategoryType(param){
        this.tradeCategory = param
        let elements = document.getElementsByClassName("tradeCategoryButton")
        for(var i=0;i<elements.length;i++){
          if(elements[i].id == param){
            elements[i].className = "btn btn-primary tradeCategoryButton"
          }
          else{
            elements[i].className = "btn btn-outline-primary tradeCategoryButton"
          }
        }
      },
      changeOrderType(param){
        this.orderType = param
        let elements = document.getElementsByClassName("orderTypeButton")
        for(var i=0;i<elements.length;i++){
          if(elements[i].id == param){
            elements[i].className = "btn btn-primary orderTypeButton"
          }
          else{
            elements[i].className = "btn btn-outline-primary orderTypeButton"
          }
        }
      },
      changeTakePrice(param){
        let elements = document.getElementsByClassName("takePriceButton")
        for(var i=0;i<elements.length;i++){
          if(elements[i].id == param){
            this.userprice = eval(`(this.${elements[i].id})`)
            if(param == "Current"){
              this.userprice = this.closepriceNear
            }
            elements[i].className = "btn btn-primary takePriceButton"
          }
          else{
            elements[i].className = "btn btn-outline-primary takePriceButton"
          }
        }
        this.takeprice = param
      }
    }
  }
</script>
