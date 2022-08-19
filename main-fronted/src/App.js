// import './App.css';
import Nav from "./components/Nav";
import IndexPage from "./page/IndexPage";
import WelcomePage from "./page/WelcomePage";
import PostPage from "./page/PostPage";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ContactPage from "./page/ContactPage";
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