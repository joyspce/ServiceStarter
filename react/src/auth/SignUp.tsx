import React from 'react';
import { connectWithoutDone } from 'app/core/connection';
import { bindActionCreators } from 'redux';
import * as authActions from 'auth/Auth.action';

class SignUp extends React.Component<any> {

  state = {
    username: '',
    email: '',
    password: ''
  }

  signUp() {
    const { AuthActions } = this.props;
    AuthActions.signUp(this.state.username, this.state.email, this.state.password)
    .then(()=>console.log('성공'))
    .catch(()=>console.log('실패'))
  }

  render() {
    return <div>
      <div><input type="text" value={this.state.username} onChange={(e)=> this.setState({username: e.target.value})} /></div>
      <div><input type="email" value={this.state.email} onChange={(e)=> this.setState({email: e.target.value})} /></div>
      <div><input type="password" value={this.state.password} onChange={(e)=> this.setState({password: e.target.value})} /></div>
      <div><button onClick={()=> this.signUp()}>가입하기</button></div>
    </div>
  }
}

export default connectWithoutDone(
  (state:any)=>({}),
  (dispatch:any)=>({
    AuthActions: bindActionCreators(authActions, dispatch)
  }),
  SignUp
);