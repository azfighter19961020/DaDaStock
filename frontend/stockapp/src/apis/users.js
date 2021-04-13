import axios from 'axios'
import {host,port} from './constant.js'

export function login(data){
  return axios.post(`http://${host()}:${port()}/api/login`,data)
}

export function register(data){
  return axios.post(`http://${host()}:${port()}/api/user`,data)
}

export function getUserData(username,token){
  return axios.get(`http://${host()}:${port()}/api/user/${username}`,{
    headers: {
      "AUTHORIZATION":token
    }
  })
}

export function fixUserData(token,data){
  return axios.put(`http://${host()}:${port()}/api/user`,data,{
    headers: {
      "AUTHORIZATION":token
    }
  })
}

export function storeBalance(token,data){
  return axios.put(`http://${host()}:${port()}/api/user/balanceAPI`,data,{
    headers: {
      "AUTHORIZATION":token
    }
  })
}