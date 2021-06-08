<template src="@/assets/stock/template.html"></template>
<style scoped src="@/assets/css/singleStock.css"></style>
<script>
  import {candleOption,splitData,calculateMA} from '@/charts/candleStick.js'
  import {specifyStock} from '@/apis/stock.js'
  import {LetterCube} from 'vue-loading-spinner'
  export default({
    name:'index',
      data(){
        return {
          login:false,
          data0:null,
          KChart:null,
          data1:null,
          isLogin:false,
          username:'',
          stockno:'',
          isLoading:false,
        }
      },
      components: {
        LetterCube
      },
      methods:{
        logout(){
          window.localStorage.removeItem("token")
          window.localStorage.removeItem("username")
          window.location.reload()
        },
        renderOrderPage(){
          window.location.href = "/stockapp/#/order/" + this.stockno
        },
        toSearch(){
          let stockno = document.getElementById('stockno').value
          if(!stockno){return}
          window.location.href = `/stockapp/#/stock/${stockno}`
          window.location.reload()
        },
      },
      mounted(){
        this.isLoading = true
        this.isLogin = window.localStorage.getItem("username") != null & window.localStorage.getItem("token") != null
        this.username = window.localStorage.getItem("username")
        this.KChart = this.$echarts.init(document.getElementById("chartContainer"))
        this.stockno = this.$route.params.stockno
        specifyStock(this.stockno).then(
          (response) => {
            if(response.data.status == 200){
              
              let datar = []
              let d = []
              for(var i=0;i<response.data.data.length;i++){
                d = []
                for(var j=2;j<response.data.data[0].length;j++){
                  d.push(response.data.data[i][j])
                }
                datar.push(d)
              }
              this.data1 = JSON.parse(JSON.stringify(datar))
              this.data0 = splitData(datar)
              this.KChart.setOption(candleOption(this.stockno,calculateMA,this.data0))
              let information = document.getElementById("information")
              let stockinf = response.data.inf
              information.innerHTML += `
                <h2>
                    ${this.stockno} : ${stockinf.stockname}
                </h2>
                ${stockinf.companyInf}
              `

            }
            else{
              let html = `
                <div><h1>Oops! ...查無股票資料</h1></div>
                <div><h2>目前這支股票沒有相關資料喔</h2></div>
                <div><button class="btn btn-primary" onclick="window.location.href='/stockapp/#/';window.location.reload()">點我回首頁</button></div>
              `
              let element = document.getElementById('app')
              element.innerHTML = html
            }
            this.isLoading = false
          }
        )
      },
    })
</script>
