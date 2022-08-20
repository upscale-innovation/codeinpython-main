import React from 'react'
import Contact from "../../components/contact/Contact"
import LeftSide from '../../components/common/leftSide/LeftSide';
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