// import './App.css';

import IndexPage from "./page/indexPage/IndexPage";
import WelcomePage from "./page/welcomPage/WelcomePage";
import PostPage from "./page/postPage/PostPage";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ContactPage from "./page/contactPage/ContactPage";
import PrivateRoute from './services/PrivateRoute'
import SignInPage from "./page/SignPage/SignInPage";
import { useDispatch } from "react-redux";
import { UserSignIn } from "./redux/userSlice";
function App() {

  const dispatch=useDispatch()
  let token = localStorage.getItem('token')
  token && dispatch(UserSignIn(JSON.parse(token)))

return (
  <Router>
    <div className="App">

    
      <Routes>
        {/* PUBLIC ROUTES */}
        <Route exact path="/" element={<WelcomePage />}/>
        <Route exact path="/signin" element={<SignInPage />}/>
        {/* AUTHENTICATED ROUTES */}
        <Route exact path="/home" element={<PrivateRoute><IndexPage /></PrivateRoute>}/>
        <Route exact path="/post-detail" element={<PostPage />}/>
        <Route exact path="/contact" element={<ContactPage/>}/>
      </Routes>
    </div>
  </Router>
);
}

export default App;