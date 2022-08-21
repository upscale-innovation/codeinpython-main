import axios from 'axios'

const baseURL = 'http://localhost:8000'

// Define TOKEN 
let token
if (typeof window !== 'undefined') {
    // Perform localStorage action
    token = localStorage.getItem('token')   
  }

const axiosInstance=axios.create({baseURL,
headers:{Authorization:'token'}})


axiosInstance.interceptors.request.use( async config => {
    //NO TOKEN
       
    if (config.headers.Authorization === "Bearer undefined"){
        token=localStorage.getItem('token') ? JSON.parse(localStorage.getItem('token')): null
        config.headers.Authorization=`Bearer ${token?.access}`
        // console.log('intercept sasns token')
        
        //  console.log({'request':config})
        return config
    } 
})
export default axiosInstance
