import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
function LeftSide() {
  return (
    <div>
      <div id="colorlib-page">
        <a href="#" class="js-colorlib-nav-toggle colorlib-nav-toggle">
          <i></i>
        </a>
        <aside id="colorlib-aside" role="complementary" class="js-fullheight">
          <nav id="colorlib-main-menu" role="navigation">
            <ul>
              <li>
                <Link to="/home">Home</Link>
              </li>
              <li class="colorlib">
                <Link to="/home">Fashion</Link>
              </li>
              <li>
                <Link to="/home">Travel</Link>
              </li>
              <li>
                <Link to="/contact">Contact</Link>
              </li>
            </ul>
          </nav>

          <div class="colorlib-footer">
            <h1 id="colorlib-logo" class="mb-4">
              <a href="index.html">
                Andrea <span>Moore</span>
              </a>
            </h1>
            <div class="mb-4">
              <h3>Subscribe for newsletter</h3>
              <form action="#" class="colorlib-subscribe-form">
                <div class="form-group d-flex">
                  <div class="icon">
                    <span class="icon-paper-plane"></span>
                  </div>
                  <input
                    type="text"
                    class="form-control"
                    placeholder="Enter Email Address"
                  />
                </div>
              </form>
            </div>
            <p class="pfooter">
              Copyright &copy;
              <script>document.write(new Date().getFullYear());</script> All
              rights reserved | This template is made with{" "}
              <i class="icon-heart" aria-hidden="true"></i> by{" "}
              <a href="https://colorlib.com" target="_blank">
                Colorlib
              </a>
            </p>
          </div>
        </aside>
      </div>
    </div>
  );
}

export default LeftSide;
