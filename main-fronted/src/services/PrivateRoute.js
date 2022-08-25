
import { useSelector } from 'react-redux'
import {Navigate } from 'react-router-dom'
import { isTokenAvailable } from '../redux/userSlice';


const PrivateRoute = ({children, ...rest})=>{
  
    const isUserLoggedIn= useSelector(isTokenAvailable);




    return !isUserLoggedIn ? <Navigate to='/signin'/> : children

}


export default PrivateRoute