import axios from 'axios'
import {host,port} from './constant.js'

export function getOrder(data,token){
  return axios.get(`http://${host()}:${port()}/api/order`,{
    params:data,
    headers: {
      "AUTHORIZATION":token
    }
    })
}

export function cancelOrder(data){
  return axios.put(`http://${host()}:${port()}/api/order`,data)
}

export function createOrder(data){
  return axios.post(`http://${host()}:${port()}/api/order`,data)
}