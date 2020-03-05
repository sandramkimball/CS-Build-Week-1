import React, { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
// import dragon from "./reddragon.jpg"
// import { createGlobalStyle } from "styled-components";
import "./login.css";
// const GlobalStyles = createGlobalStyle`
//   @import url('https://fonts.googleapis.com/css?family=Press+Start+2P&display=swap');
//   body {
//     font-family: 'Notable', sans-serif;
//   }
// `;

export default function Login(props) {
  const [state, setState] = useState({
    username: "",
    password: ""
  });

  const changeHandler = e => {
    setState({
      ...state,
      [e.target.name]: e.target.value
    });
  };

  const submitHandler = (e, state) => {
    e.preventDefault();
    axios
      .post("https://lambda-mud-test.herokuapp.com/api/login/", state)
      .then(res => {
        console.log("RESPONSE", res);
        localStorage.setItem("token", res.data.key);
        props.history.push("/mainpage");
      })
      .catch(err => {
        console.log(err);
      });
    setState({
      username: "",
      password: ""
    });
  };

  return (
    <div className="wrapper">
      <div className="signup-text">{/* <GlobalStyles /> */}</div>
      <form
        style={{
          textAlign: "center",
          background: "#2d2db7",
          height: "620px",
          width: "100%",
          height: "100vh"
        }}
        onSubmit={e => submitHandler(e, state)}
      >
        <div>
          <div className="title"> Sign in to your account </div>
          {/* <img src={dragon} style={{ width: "7.5rem" }} /> */}

          <div className="label"> Username </div>
          <input
            type="text"
            name="username"
            placeholder="Enter Username"
            value={state.username}
            onChange={changeHandler}
            required
          />
        </div>
        <div>
          <div className="label"> Password </div>
          <input
            type="password"
            name="password"
            value={state.password}
            onChange={changeHandler}
            placeholder="Enter Password"
            required
          />
        </div>
        <button
          className="signup-btn"
          style={
            state.email && state.password
              ? { backgroundColor: "blue" }
              : {
                  color: "black",
                  backgroundColor: "f3f5f1",
                  fontWeight: "bold",
                  marginTop: "20px"
                }
          }
        >
          Login
        </button>
        <div>
          <div className="bottom">Don't have an account?</div>
          <div>
            <Link to="/registration">
              <div className="signup">SIGN UP</div>
            </Link>
          </div>
        </div>
      </form>
    </div>
  );
}

// const Title = styled.h1`
//   font-size: 1.5em;
//   text-align: center;
//   color: #f5f5f3;
//   margin-top: 0px;
//   padding-top: 50px;
//   font-family: "Press Start 2P", cursive;
//   padding-bottom: 60px;
// `;
// const Label = styled.h1`
//   font-size: 1em;
//   text-align: center;
//   color: white;
//   padding-top: 10px;
//   font-family: "Press Start 2P", cursive;
// `;
// const Bottom = styled.h1`
//   font-size: 1em;
//   text-align: center;
//   color: red;
//   padding-top: 28px;
//   font-family: "Press Start 2P", cursive;
// `;
// const Signup = styled.h1`
//   font-size: 1em;
//   text-align: center;
//   color: red;
//   padding-top: 5px;
//   font-family: "Press Start 2P", cursive;
// `;
