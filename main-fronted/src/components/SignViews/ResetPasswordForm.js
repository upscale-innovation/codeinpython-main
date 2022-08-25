import React, { useState } from "react";
import { useForm } from "react-hook-form";

import axiosInstance from "../../services/axiosInterceptor";

import { useNavigate } from "react-router-dom";
const ResetPasswordForm = () => {



const navigate=useNavigate()
const [errorStatus,setErrorStatus]=useState("")


  const {
    register,
    handleSubmit,
 
  } = useForm();




  const onSubmit = async(data) => {
    
    const login= await axiosInstance.post("http://localhost:8000/reset_password",{new_password:data.new_password,confirm_password:data.confirm_password}).catch(error => setErrorStatus(JSON.parse(error.request.responseText).message))
    const response= await login.data
  
    if (response.success === "true")
    {
        navigate('/home')
        } 
}


  

  return (
    <div className=" max-w-xs  md:max-w-sm w-screen border p-4">
      <form className="flex flex-col " onSubmit={handleSubmit(onSubmit)}>
        <div className="flex  items-center">

          <div className=" flex-grow">
            <label className="text-sm">New Password</label>
            <input
              type="password"
              className="border  p-1 w-full"
              {...register("new_password")}
              placeholder="Enter your new password"
            />
          </div>
        </div>

        <div className="flex justify-between pt-4 items-center ">
          <label>Confirm your Password</label>
          
        </div>
        <input
          type="password"
          className="border  p-1 mb-4"
          placeholder="Confirm your password"
          {...register("confirm_password")}
        />

        <button className=" bg-yellowBase text-white py-2 mt-2">Reset your Password</button>
      </form>
      {errorStatus && <p className=" text-red-600 pt-4"> Error : {errorStatus}</p> }
      
    </div>
  );
};

export default ResetPasswordForm;
