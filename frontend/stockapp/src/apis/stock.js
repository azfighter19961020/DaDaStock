import axios from 'axios'
import {host,port} from './constant.js'

export function randomStock(){
  return axios.post(`http://${host()}:${port()}/api/stockday`)
}

export function TSEapi(){
  //reverse
  let date1 = new Date(Date.now()) / 1000
  let date2 =  new Date('2020-09-09') / 1000
  return axios.get(`https://ws.api.cnyes.com/ws/api/v1/charting/history?symbol=TWS:TSE01:INDEX&resolution=D&quote=1&from=${date1}&to=${date2}`)
}

export function specifyStock(stockno){
  return axios.post(`http://${host()}:${port()}/api/stockday/${stockno}`)
}

export function getClosePriceNear(stockno){
  return axios.post(`http://${host()}:${port()}/api/stocks/${stockno}/closeprice`)
}