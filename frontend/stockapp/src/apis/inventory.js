import axios from 'axios'
import {host,port} from './constant.js'

export function getInventory(token,data){
  console.log(token)
  return axios.post(`http://${host()}:${port()}/api/inventory`,data,{
    headers: {
      "AUTHORIZATION":token
    }
  })
}