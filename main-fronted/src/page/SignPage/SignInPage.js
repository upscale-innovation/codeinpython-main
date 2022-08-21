import React, { useState } from 'react'
import FormView from '../../components/SignViews/FormView'
import NavView from '../../components/SignViews/NavView'
import SignUpView from '../../components/SignViews/SignUpView'

const SignInPage = () => {
  const [signUp,setSignUp]=useState(false)
  const handleSignUpScreen=()=>{
    setSignUp(true)
  }
  return (
    <div className='relative h-screen w-screen '>
        
    {/* SIGN NAV BAR */}
    <NavView handleSignUpScreen={handleSignUpScreen}/>
    {/* SIGN WITH GOOGLE */}
    {/* SIGN WITH GITHUB */}
    {/* SIGN WITH FACEBOOK */}
    {/* SIGN FORM */}
    <div className=' absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] '>
    {
      !signUp ? ( <FormView/>):(<SignUpView/>)
    }
   

    </div>


    </div>
  )
}

export default SignInPage