// import './App.css';
import React from "react";
import IndexPage from "./page/indexpage/IndexPage";
import WelcomePage from "./page/welcomepage/WelcomePage";
import PostPage from "./page/postpage/PostPage";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ContactPage from "./page/contactpage/ContactPage";
function App() {
return (
  <Router>
    <div className="App">
      <Routes>
        <Route exact path="/" element={<WelcomePage />}></Route>
        <Route exact path="/home" element={<IndexPage />}></Route>
        <Route exact path="/post-detail" element={<PostPage />}></Route>
        <Route exact path="/contact" element={<ContactPage/>}></Route>
      </Routes>
    </div>
  </Router>
);
}

export default App;