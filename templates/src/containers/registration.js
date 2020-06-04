import React from 'react';
import {Helmet} from 'react-helmet';
import {Link} from 'react-router-dom';

import OwlCarousel from 'react-owl-carousel2';
import 'react-owl-carousel2/src/owl.carousel.css';

import image from '../images/lab-login.svg';

import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import LoginForm from "../components/login_form";
import SignUpForm from "../components/signup_form";


class Registration extends React.Component {
    constructor(props) {
        super(props);
        this.owl = React.createRef();
        this.state = {
            title: "ورود",
        };
    }

    componentDidMount() {
        if (this.props.type === "signup") {
            return this.signUpShow();
        }
        // Functions.inputFocus();
    }

    loginShow = () => {
        this.owl.current.prev();
        this.setState({title: "ورود"});
    };

    signUpShow = () => {
        this.owl.current.next();
        this.setState({title: "ثبت نام"});
    };

    render() {
        const options = {
            items: 1,
            nav: false,
            loop: false,
            margin: 10,
            dots: false,
            touchDrag: false,
            mouseDrag: false,
        };
        return (
            <div>
                <Helmet>
                    <title>{this.state.title}</title>
                </Helmet>
                <Card className="two-side fixed">
                    <Card.Body className="p-0">
                        <Row>
                            <Col>
                                <OwlCarousel ref={this.owl} options={options}>
                                    <div className="item">
                                        <LoginForm />
                                        <hr/>
                                        <div className="text-center">
                                            <span>کاربر جدید هستید؟</span>
                                            <Link onClick={this.signUpShow} to="/signup">
                                                عضویت
                                            </Link>
                                        </div>
                                    </div>
                                    <div className="item">
                                        <SignUpForm />
                                        <hr/>
                                        <div className="text-center">
                                            <Link onClick={this.loginShow} to="/login">
                                                وارد شوید
                                            </Link>
                                        </div>
                                    </div>
                                </OwlCarousel>
                            </Col>
                            <Col>
                                <img src={image} alt="Login"/>
                            </Col>
                        </Row>
                    </Card.Body>
                </Card>
            </div>
        );
    }
}

export default Registration;