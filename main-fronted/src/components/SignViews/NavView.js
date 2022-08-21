import React from "react";
import { MenuIcon, SearchIcon } from "@heroicons/react/outline";
import { useDispatch, useSelector } from "react-redux";
import { isTokenAvailable, UserSignOut } from "../../redux/userSlice";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
const NavView = ({handleSignUpScreen}) => {

 let user = useSelector(isTokenAvailable)
  const dispatch=useDispatch()
  const navigate=useNavigate()
  return (
    <div className="p-2 border border-b-0 border-gray-400 shadow-md flex space-x-4 justify-center items-center z-10">
      <MenuIcon className="h-5 w-5  text-gray-500" />
      <nav>
       
        <Link to="/"><p className="text-[#f5a425] font-semibold text-lg whitespace-nowrap"> 
        GRAD SCHOOL
      </p></Link>
      </nav>
      
      <div className=" space-x-2 hidden md:flex">
        <p>About</p>
        <p>Products</p>
        <p className=" whitespace-nowrap">For Teams</p>
      </div>

      <div className=" max-w-screen-sm w-full border border-gray-400 items-center px-2 hidden md:flex rounded-sm">
        <SearchIcon className="h-5 w-5  text-gray-500" />
        <input placeholder="Search.. " className=" text-sm p-2 w-full outline-none" />
      </div>
      {!user ? ( <button onClick={()=>{handleSignUpScreen()}} className=" py-1 px-2 text-sm border-[#f5a425]  border-2 rounded-md cursor-pointer hover:opacity-70 whitespace-nowrap">
        Sign Up
      </button>):( <button onClick={()=>{dispatch(UserSignOut());navigate("/")}} className=" py-1 px-2 text-sm border-[#f5a425]  border-2 rounded-md cursor-pointer hover:opacity-70 whitespace-nowrap">
        Sign Out
      </button>)}
     
    </div>
  );
};

export default NavView;
