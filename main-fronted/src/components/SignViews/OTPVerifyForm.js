
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import axiosInstance from "../../services/axiosInterceptor";
import axios from 'axios'
import { UserSignIn } from "../../redux/userSlice";
import { useNavigate } from "react-router-dom";
const OTPVerifyForm = () => {

const dispatch=useDispatch()
const navigate=useNavigate()
const [errorStatus,setErrorStatus]=useState("")


  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();




  const onSubmit = async(data) => {
    const login= await axios.post("http://localhost:8000/forget_password",{country_code:data.countryCode,mobile_number:data.mobileNumber,otp:data.otp}).catch(error => setErrorStatus(JSON.parse(error.request.responseText).message))
    const response= await login.data
   
    if (response.success === true)
    {
        dispatch(UserSignIn(response.data.authorization));
        localStorage.setItem("token",JSON.stringify(response.data.authorization))
        navigate('/home')

        } 
}

console.log("error",errorStatus)
  
  return (
    <div className=" max-w-xs  md:max-w-sm w-screen border p-4 space-y-4">
    <form className="flex flex-col " onSubmit={handleSubmit(onSubmit)}>
      <p className=" text-xs pb-4">You already received an OTP password?  Enter your OTP number to connect to your session and change your password</p>
      <div className="flex  flex-col space-y-4">
          <div className="flex ">
        <div className=" ">
          <label className="text-sm">Code</label>
          <input
            type="tel"
            className="border  p-1 w-10 "
            {...register("countryCode")}
            placeholder=" +11"
          />
        </div>
        <div className=" flex-grow">
          <label className="text-sm">Phone Number</label>
          <input
            type="tel"
            className="border  p-1 w-full"
            {...register("mobileNumber")}
            placeholder="679862200"
          />
        </div>
          </div>

        <div>
      
          <label className="text-sm">OTP Password</label>
          <input
            type="tel"
            className="border  p-1 w-full"
            {...register("otp")}
            placeholder="OTP Number ..."
          />
  
        </div>
      </div>



      <button className=" bg-yellowBase text-white py-2 mt-4">Send Recovery Phone Number</button>
    </form>
    {errorStatus && <p className=" text-red-600 pt-4"> Error : {errorStatus}</p> }
    
  </div>
  )
}

export default OTPVerifyForm