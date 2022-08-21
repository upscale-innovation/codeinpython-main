import React from 'react'
import FormView from '../../components/SignViews/FormView'
import NavView from '../../components/SignViews/NavView'

const SignInPage = () => {
  return (
    <div className='relative h-screen w-screen '>
        
    {/* SIGN NAV BAR */}
    <NavView/>
    {/* SIGN WITH GOOGLE */}
    {/* SIGN WITH GITHUB */}
    {/* SIGN WITH FACEBOOK */}
    {/* SIGN FORM */}
    <div className=' absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] '>
    <FormView/>

    </div>


    </div>
  )
}

export default SignInPage