import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import axiosInstance from "../../services/axiosInterceptor";
import axios from 'axios'
import { UserSignIn } from "../../redux/userSlice";
import { useNavigate } from "react-router-dom";
const FormView = () => {


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
    const login= await axios.post("http://localhost:8000/login",{country_code:data.countryCode,mobile_number:data.mobileNumber,password:data.password}).catch(error => setErrorStatus(JSON.parse(error.request.responseText).message))
    const response= await login.data
   
    if (response.success === true)
    {
        dispatch(UserSignIn(response.data.authorization));
        localStorage.setItem("token",JSON.stringify(response.data.authorization))
        navigate('/home')

        } 
}


  

  return (
    <div className=" max-w-xs  md:max-w-sm w-screen border p-4">
      <form className="flex flex-col " onSubmit={handleSubmit(onSubmit)}>
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

        <div className="flex justify-between pt-4 items-center ">
          <label>Password</label>
          <p  onClick={()=>{navigate("/accoutRecovery")}} className=" text-xs text-yellowBase cursor-pointer">Forgot password ?</p>
        </div>
        <input
          type="password"
          className="border  p-1 mb-4"
          {...register("password")}
        />

        <button className=" bg-yellowBase text-white py-2 mt-2">Sign In</button>
      </form>
      {errorStatus && <p className=" text-red-600 pt-4"> Error : {errorStatus}</p> }
      
    </div>
  );
};

export default FormView;
