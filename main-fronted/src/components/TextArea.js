import React, { useState } from 'react'
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
function TextArea() {
    const [vote, SetVote] = useState(0)
    const upvote = () => {
        SetVote(vote+1)
    }
       const downvote = () => {
         SetVote(vote - 1);
       };
    return (
        <div>
          <div id="colorlib-main">
            <section class="ftco-section">
              <div class="container">
                <div class="row">
                  <div class="col-12">
                    <div class="blog-entry d-md-flex">
                      <div class="text text-2 pl-md-4">
                        <h3 class="mb-2">
                          <a href="single.html">
                            A Loving Heart is the Truest Wisdom
                          </a>
                        </h3>
                        <div class="meta-wrap">
                          <p class="meta">
                            <span>
                              <i class="icon-calendar mr-2"></i>June 28, 2019
                            </span>
                            <span>
                              <a href="single.html">
                                <i class="icon-folder-o mr-2"></i>Travel
                              </a>
                            </span>
                            <span>
                              <i class="icon-comment2 mr-2"></i>5 Comment
                            </span>
                          </p>
                        </div>
                        <div class="row">
                          <div class="col-1">
                            <span>
                              <button
                                onClick={upvote}
                                className="btn btn-default"
                              >
                                <i class="fa fa-caret-up"></i>
                              </button>

                              {vote}
                              <button
                                onClick={downvote}
                                className="btn btn-default"
                              >
                                <i class="fa fa-caret-down"></i>
                              </button>
                            </span>
                          </div>
                          <div class="col">
                            <p class="mb-4">
                              A small river named Duden flows by their place and
                              supplies it with the necessary regelialia.
                            </p>
                            <p>
                              <Link to="/post-detail">Read More</Link>

                              <span class="ion-ios-arrow-forward"></span>
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col text-center text-md-left">
                    <div class="block-27">
                      <ul>
                        <li>
                          <a href="#">&lt;</a>
                        </li>
                        <li class="active">
                          <span>1</span>
                        </li>
                        <li>
                          <a href="#">2</a>
                        </li>
                        <li>
                          <a href="#">3</a>
                        </li>
                        <li>
                          <a href="#">4</a>
                        </li>
                        <li>
                          <a href="#">5</a>
                        </li>
                        <li>
                          <a href="#">&gt;</a>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
    );
}

export default TextArea