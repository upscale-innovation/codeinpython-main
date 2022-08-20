import React from 'react'
import LeftSide from '../../components/common/leftside/LeftSide'
import PostDetail from '../../components/postdetail/PostDetail'
import RightSide from "../../components/common/rightside/RightSide";
function PostPage() {
  return (
    <div>
      <div className="row">
        <div className="col-3">
          <LeftSide />
        </div>
        <div className="col-6">
          <PostDetail />
        </div>
        <div className="col-3">
          <RightSide />
        </div>
      </div>
    </div>
  );
}

export default PostPage