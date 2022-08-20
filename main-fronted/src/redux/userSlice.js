import { createSlice } from '@reduxjs/toolkit'
import jwt_decode from 'jwt-decode';






const initialState = {
  token: null,
  user:null,
}

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {

    UserSignIn: (state, action) => {
      state.token=action.payload
      state.user= jwt_decode(state.token?.access)
     
    
    },
    UserSignOut: (state, action) => {
      state.token=null
      state.user= null
      localStorage.removeItem("token")

     
    
    },
  },
})

// Action creators are generated for each case reducer function
export const { UserSignIn,UserSignOut } = userSlice.actions
export const isTokenAvailable = (state) => state.user.token;
export const isUserLoggedIn = (state) => state.user.user;



export default userSlice.reducer