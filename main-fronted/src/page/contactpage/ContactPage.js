import React from 'react'
import Leftside from '../../components/common/leftside/LeftSide'
import Contact from "../../components/contact/Contact";
function ContactPage() {
  return (
    <div>
      <div className="row">
        <div className="col-1">
          <Leftside />
        </div>
        <div className="col-10">
          <Contact />
        </div>
      </div>
    </div>
  );
}

export default ContactPage