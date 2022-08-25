import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import axiosInstance from "../../services/axiosInterceptor";
import axios from 'axios'
import { UserSignIn } from "../../redux/userSlice";
import { useNavigate } from "react-router-dom";
import AccountRecoveryform from "../../components/SignViews/AccountRecoveryForm";
import OTPVerifyForm from "../../components/SignViews/OTPVerifyForm";
const RecoveryPage = () => {


    




  

  return (
    <div className="flex justify-center items-center h-screen flex-col space-y-4">
<AccountRecoveryform/>
    <p>OR</p>
    
<OTPVerifyForm/>
    
    </div>
   
  );
};

export default RecoveryPage;
