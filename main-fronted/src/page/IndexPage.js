import React from 'react'
import LeftSide from '../components/LeftSide';
import RightSide from '../components/RightSide';
import TextArea from '../components/TextArea';
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
function IndexPage() {
  return (
    <div>
      <div className="row">
        <div className="col-1">
          <LeftSide />
        </div>
        <div className="col-8">
          <TextArea />
        </div>
        <div className="col-3">
            <RightSide />
        </div>
      </div>
    </div>
  );
}

export default IndexPage