// import './App.css';
import Nav from "./components/common/nav/Nav";
import IndexPage from "./page/indexPage/IndexPage";
import WelcomePage from "./page/welcomPage/WelcomePage";
import PostPage from "./page/postPage/PostPage";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ContactPage from "./page/contactPage/ContactPage";
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