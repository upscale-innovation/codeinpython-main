import React from 'react'
import LeftSide from '../../components/common/leftSide/LeftSide';
import RightSide from '../../components/common/rightSide/RightSide';
import TextArea from '../../components/common/textArea/TextArea';
import NavView from '../../components/SignViews/NavView';
import { useDispatch } from 'react-redux';
import { UserSignIn } from '../../redux/userSlice';
function IndexPage() {
  const dispatch=useDispatch()
  let token = localStorage.getItem('token')
  token && dispatch(UserSignIn(JSON.parse(token)))

  return (
    <div>
      <NavView/>
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
    </div>

  );
}

export default IndexPage