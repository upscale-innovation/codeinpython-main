// import './App.css';


import IndexPage from "./page/indexPage/IndexPage";
import WelcomePage from "./page/welcomPage/WelcomePage";
import PostPage from "./page/postPage/PostPage";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ContactPage from "./page/contactPage/ContactPage";
import PrivateRoute from './services/PrivateRoute'
import SignInPage from "./page/SignPage/SignInPage";
import { useDispatch, useSelector } from "react-redux";
import { isTokenAvailable, UserSignIn, UserSignOut } from "./redux/userSlice";
import RecoveryPage from "./page/AccountRecoveryPage/RecoveryPage";
import ResetPasswordPage from "./page/ResetPasswordPage/ResetPasswordPage";
import dayjs from 'dayjs'
import jwtDecode from "jwt-decode";
function App() {

  const dispatch=useDispatch()
  let token = localStorage.getItem('token') ?  JSON.parse(localStorage.getItem('token')): null

  
if (token){
let tokenExpirationDate= token ? (jwtDecode(token)).exp:(null)  
const isTokenExpired= dayjs.unix(tokenExpirationDate).diff(dayjs())<1

isTokenExpired&&dispatch(UserSignOut())
!isTokenExpired&& dispatch(UserSignIn(token))
}



return (
  <Router>
    <div className="App">

    
      <Routes>
        {/* PUBLIC ROUTES */}
        <Route exact path="/" element={<WelcomePage />}/>
        <Route exact path="/signin" element={<SignInPage />}/>
        <Route exact path="/accoutRecovery" element={<RecoveryPage />}/>
        {/* AUTHENTICATED ROUTES */}
        <Route exact path="/home" element={<PrivateRoute><IndexPage /></PrivateRoute>}/>
        <Route exact path="/ResetPassword" element={<PrivateRoute><ResetPasswordPage /></PrivateRoute>}/>
        <Route exact path="/post-detail" element={<PostPage />}/>
        <Route exact path="/contact" element={<ContactPage/>}/>
      </Routes>
    </div>
  </Router>
);
}

export default App;