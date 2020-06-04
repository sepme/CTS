import React from 'react';
import {
    BrowserRouter as Router,
    Route,
    Link
} from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css'
import './App.css';
import Registration from './containers/registration';
import RecoverPass from './containers/recocer_pass';
import Switch from "react-bootstrap/esm/Switch";

function App() {
    return (
        <Router>
            <div className="App">
                <Switch>
                    <Route path="/login">
                        <Registration type="login"/>
                    </Route>
                    <Route path="/signup">
                        <Registration type="signup"/>
                    </Route>
                    <Route path="/recover_password">
                        <RecoverPass>
                            <Link to="/login">
                                بازگشت به صفحه ورود
                            </Link>
                        </RecoverPass>
                    </Route>
                </Switch>
            </div>
        </Router>
    );
}

export default App;
