import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import axiosInstance from "../../services/axiosInterceptor";
import axios from 'axios'
import { UserSignIn } from "../../redux/userSlice";
import { useNavigate } from "react-router-dom";
const AccountRecoveryform = () => {


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
    const login= await axios.post("http://localhost:8000/forget_password",{country_code:data.countryCode,mobile_number:data.mobileNumber}).catch(error => setErrorStatus(JSON.parse(error.request.responseText).message))
    const response= await login.data
   
    if (response.success === true)
    {
       
        navigate('/')

        } 
}


  

  return (

 <div className=" max-w-xs  md:max-w-sm w-screen border p-4">
      <form className="flex flex-col " onSubmit={handleSubmit(onSubmit)}>
        <p className=" text-xs pb-4">Forgot your phone’s password ?  Enter your phone number and we’ll send you a OTP recovery number.</p>
        <div className="flex  items-center">
            
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

 

        <button className=" bg-yellowBase text-white py-2 mt-4">Send Recovery Phone Number</button>
      </form>
      {errorStatus && <p className=" text-red-600 pt-4"> Error : {errorStatus}</p> }
      
    </div>

    

    

   
  );
};

export default AccountRecoveryform;
