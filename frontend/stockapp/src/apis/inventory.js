import axios from 'axios'
import {host,port} from './constant.js'

export function getInventory(token,data){
  return axios.post(`http://${host()}:${port()}/api/inventory`,data,{
    headers: {
      "AUTHORIZATION":token
    }
  })
}
