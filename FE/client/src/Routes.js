import React from "react";
// import Dashboard from "./components/Dashboard";
import { Route, Switch, BrowserRouter } from "react-router-dom";
import Login from "./authentication/Login";
// import Register from "./authentication/Register";
// import PrivateRoute from "./authentication/PrivateRoute";
import Signup from "./components/Signup/Signup";
import Main from "./components/Main/Main";

function Routes(props) {
  return (
    <div>
      <BrowserRouter>
        <Switch>
          <Route exact path="/" render={props => <Login {...props} />} />
          <Route path="/registration" render={props => <Signup {...props} />} />
          <Route path="/mainpage" render={props => <Main {...props} />} />
          {/* <PrivateRoute exact path="/" component={Dashboard} /> */} */}
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default Routes;
