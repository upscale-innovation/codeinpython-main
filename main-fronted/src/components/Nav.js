import React from 'react'
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
function Nav() {
  return (
    <div>
      <header class="main-header clearfix" role="header">
        <div class="logo">
          <a href="#">
            <em>Grad</em> School
          </a>
        </div>
        <a href="#menu" class="menu-link">
          <i class="fa fa-bars"></i>
        </a>
        <nav id="menu" class="main-nav" role="navigation">
          <ul class="main-menu">
            <li>
              <a href="#section1">Home</a>
            </li>
            <li class="has-submenu">
              <a href="#section2">About Us</a>
              <ul class="sub-menu">
                <li>
                  <a href="#section2">Who we are?</a>
                </li>
                <li>
                  <a href="#section3">What we do?</a>
                </li>
                <li>
                  <a href="#section3">How it works?</a>
                </li>
                <li>
                  <a
                    href="https://templatemo.com/about"
                    rel="sponsored"
                    class="external"
                  >
                    External URL
                  </a>
                </li>
              </ul>
            </li>
            <li>
              <a href="#section4">Courses</a>
            </li>
            <li>
              <a href="#section6">Contact</a>
            </li>
            <li>
              <a href="https://templatemo.com" class="external">
                External
              </a>
            </li>
          </ul>
        </nav>
      </header>
      <section class="section main-banner" id="top" data-section="section1">
        <video autoplay muted loop id="bg-video">
          <source src="assets/images/course-video.mp4" type="video/mp4" />
        </video>

        <div class="video-overlay header-text">
          <div class="caption">
            <h6>Graduate School of Management</h6>
            <h2>
              <em>Your</em> Classroom
            </h2>
            <div>
              <div class="scroll-to-section">
               
                <Link to='/home'>
                   <button className='btn btn-success btn-lg'>Login .....</button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

  <section class="features">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 col-12">
          <div class="features-post">
            <div class="features-content">
              <div class="content-show">
                <h4><i class="fa fa-pencil"></i>All Courses</h4>
              </div>
              <div class="content-hide">
                <p>Curabitur id eros vehicula, tincidunt libero eu, lobortis mi. In mollis eros a posuere imperdiet. Donec maximus elementum ex. Cras convallis ex rhoncus, laoreet libero eu, vehicula libero.</p>
                <p class="hidden-sm">Curabitur id eros vehicula, tincidunt libero eu, lobortis mi. In mollis eros a posuere imperdiet.</p>
                <div class="scroll-to-section"><a href="#section2">More Info.</a></div>
            </div>
            </div>
          </div>
        </div>
        <div class="col-lg-4 col-12">
          <div class="features-post second-features">
            <div class="features-content">
              <div class="content-show">
                <h4><i class="fa fa-graduation-cap"></i>Virtual Class</h4>
              </div>
              <div class="content-hide">
                <p>Curabitur id eros vehicula, tincidunt libero eu, lobortis mi. In mollis eros a posuere imperdiet. Donec maximus elementum ex. Cras convallis ex rhoncus, laoreet libero eu, vehicula libero.</p>
                <p class="hidden-sm">Curabitur id eros vehicula, tincidunt libero eu, lobortis mi. In mollis eros a posuere imperdiet.</p>
                <div class="scroll-to-section"><a href="#section3">Details</a></div>
            </div>
            </div>
          </div>
        </div>
        <div class="col-lg-4 col-12">
          <div class="features-post third-features">
            <div class="features-content">
              <div class="content-show">
                <h4><i class="fa fa-book"></i>Real Meeting</h4>
              </div>
              <div class="content-hide">
                <p>Curabitur id eros vehicula, tincidunt libero eu, lobortis mi. In mollis eros a posuere imperdiet. Donec maximus elementum ex. Cras convallis ex rhoncus, laoreet libero eu, vehicula libero.</p>
                <p class="hidden-sm">Curabitur id eros vehicula, tincidunt libero eu, lobortis mi. In mollis eros a posuere imperdiet.</p>
                <div class="scroll-to-section"><a href="#section4">Read More</a></div>
            </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>


    </div>
  );
}

export default Nav
