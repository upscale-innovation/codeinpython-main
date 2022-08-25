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
    const login= await axios.post("http://localhost:8000/signup",{country_code:data.countryCode,mobile_number:data.mobileNumber,password:data.password,name:data.name}).catch(error => setErrorStatus(JSON.parse(error.request.responseText).message))
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
    <div className=" max-w-xs  md:max-w-lg w-screen border p-4">
      <form className="flex flex-col " onSubmit={handleSubmit(onSubmit)}>
      <div className="flex flex-grow items-center justify-center pb-4 space-x-2 ">
            <label className=" whitespace-nowrap pr-2 pt-2">Enter your Name</label>
            <input
              type="text"
              className="border  p-1 w-full "
              {...register("name")}
              placeholder=" your name .."
            />
        </div>
        <div className="flex  space-x-3 items-center">
 
          <div className="flex flex-col ">
            <label className="text-sm">Code</label>
            <input
              type="tel"
              className="border  p-1  "
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
       
        </div>
        <input
          type="password"
          className="border  p-1 mb-4"
          {...register("password")}
        />

        <button className=" bg-yellowBase text-white py-2 mt-2">Sign Up</button>
      </form>
      {errorStatus && <p className=" text-red-600 pt-4"> Error : {errorStatus}</p> }
      
    </div>
  );
};

export default FormView;
