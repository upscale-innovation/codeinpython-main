import axios from 'axios'
import jwtDecode from 'jwt-decode'
import jwt_decode from 'jwt-decode'
import dayjs from 'dayjs'


const baseURL = 'http://localhost:8000'

// Define TOKEN 
let token
if (typeof window !== 'undefined') {
    // Perform localStorage action
    token = localStorage.getItem('token')   
  }

const axiosInstance=axios.create({baseURL,
headers:{Authorization:JSON.parse(token)}})



axiosInstance.interceptors.request.use( async config => {
    //NO TOKEN
      
    if (config.headers.Authorization === "Bearer undefined"){
        token=localStorage.getItem('token') ? JSON.parse(localStorage.getItem('token')): null
        config.headers.Authorization=`${token}`
  
        
     
        return config
    } 
    return config
})
export default axiosInstance
