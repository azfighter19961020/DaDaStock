<template src="@/assets/index/template.html"></template>
<style scoped src="@/assets/css/index.css"></style>
<script>
  import {candleOption,splitData,calculateMA} from '@/charts/candleStick.js'
  import {randomStock,TSEapi} from '@/apis/stock.js'
  import {host,port} from '@/apis/constant.js'
  import {LetterCube} from 'vue-loading-spinner'
  export default({
    name:'index',
      data(){
        return {
          login:false,
          KOptions:null,
          data0:null,
          KChart:null,
          linChart:null,
          isLogin:false,
          username:'',
          randomStockNo:'',
          isLoading: false,
        }
      },
      components: {
        LetterCube
      },
      methods:{
        toOrder(){
          window.location.href=`/stockapp/#/order/${this.randomStockNo}`
        },
        logout(){
          window.localStorage.removeItem("username")
          window.localStorage.removeItem("token")
          window.location.reload()
        },
        toSearch(){
          let stockno = document.getElementById('stockno').value
          if(!stockno){return}
          window.location.href = `/stockapp/#/stock/${stockno}`
        }
      },
      async mounted(){
        this.isLoading = true
        this.isLogin = window.localStorage.getItem("username") != null & window.localStorage.getItem("token") != null
        this.username = window.localStorage.getItem("username")
        this.KChart = this.$echarts.init(document.getElementById("chartContainer"))
        this.TSEChart = this.$echarts.init(document.getElementById("otherChartContainer"))
        // 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
        let [randomResponse,TSEapiResponse] = await Promise.all([randomStock(),TSEapi()])
        this.data0 = splitData(randomResponse.data.data)
        console.log("data0:")
        console.log(this.data0)
        let stockinf = randomResponse.data.inf
        this.KChart.setOption(candleOption(stockinf.stockid,calculateMA,this.data0))
        let informationArea = document.getElementById("stockInformation")
        informationArea.innerHTML += `
          <h2>
              HotStock: ${stockinf.stockname}
          </h2>
          ${stockinf.companyInf}
          <img src="http://${host()}:${port()}/media/${stockinf.logo}" alt="" style="height:30%">
        `
        this.randomStockNo = stockinf.stockid
        let tsedata = TSEapiResponse.data.data
        let times = tsedata.t
        let openprices = tsedata.o
        let lowprices = tsedata.l
        let highprices = tsedata.h
        let closeprices = tsedata.c
        let data = []
        let date = ""
        for(var i=times.length-1;i>0;i--){
          date = new Date(parseInt(times[i]) * 1000).toLocaleString()
          data.push([
            date,
            openprices[i],
            closeprices[i],
            lowprices[i],
            highprices[i],
          ])
        }
        data = splitData(data)
        this.TSEChart.setOption(candleOption('加權指數',calculateMA,data))
        this.isLoading = false
        // randomStock().then(
        //   (response) => {
        //     if(response.data.status == 200){
        //       this.data0 = splitData(response.data.data)
        //       let stockinf = response.data.inf
        //       this.KChart.setOption(candleOption(stockinf.stockid,calculateMA,this.data0))
              
        //       let informationArea = document.getElementById("stockInformation")
        //       informationArea.innerHTML += `
        //         <h2>
        //             HotStock: ${stockinf.stockname}
        //         </h2>
        //         ${stockinf.companyInf}
        //         <img src="http://3.21.154.195:81/media/${stockinf.logo}" alt="" style="height:30%">
        //       `
        //       this.randomStockNo = stockinf.stockid
        //       TSEapi().then(
        //          (response) => {
        //            if(response.data.statusCode == 200){
                      // let times = response.data.data.t
                      // let openprices = response.data.data.o
                      // let highprices = response.data.data.h
                      // let lowprices = response.data.data.l
                      // let closeprices = response.data.data.c
                      // let data = []
                      // let date = ""
                   //    for(var i=times.length-1;i>0;i--){
                   //      date = new Date(parseInt(times[i]) * 1000).toLocaleString()
                   //      data.push([
                   //        date,
                   //        openprices[i],
                   //        closeprices[i],
                   //        lowprices[i],
                   //        highprices[i],
                   //      ])
                   //    }
                   //    data = splitData(data)
                   //    this.TSEChart.setOption(candleOption('加權指數',calculateMA,data))
                   // }
                   // else{
                   //   alert("error!")
//                   }
//                 }
//                )
//            }
//          }
//        )
        
      },
    })
</script>
