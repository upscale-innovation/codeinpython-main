import React from 'react'

import LeftSide from '../../components/common/leftSide/LeftSide';
import Contact from "../../components/contact/Contact";

function ContactPage() {
  return (
    <div>
      <div className="row">
        <div className="col-1">
          <LeftSide />
        </div>
        <div className="col-10">
          <Contact />
        </div>
      </div>
    </div>
  );
}

export default ContactPage