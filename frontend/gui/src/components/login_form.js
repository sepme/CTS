import React from 'react';
import Form from "react-bootstrap/esm/Form";
import {Link} from "react-router-dom";
import Button from "react-bootstrap/Button";
import jQuery from 'jquery';

class LoginForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            values: {
                email: "",
                password: ""
            },
            isSubmitting: false,
            isError: false
        }
    }

    handleInputChange = e =>
        this.setState({
            values: {...this.state.values, [e.target.name]: e.target.value}
        });

    submitForm = (event) => {
        event.preventDefault();
        this.setState({isSubmitting: true});
        fetch('/login_ajax/', {
            method: 'POST',
            body: JSON.stringify(this.state.values),
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            }
        })
            .then(res => {
                this.setState({isSubmitting: false});
                return res;
            })
            .then(data => {
                console.log(data);
            });
        console.log("login");
    };

    render() {
        return (
            <Form className="text-right" onSubmit={this.submitForm} id="login-ajax-form">
                <h6 className="text-right">ورود به حساب کاربری</h6>
                <Form.Group controlId="LoginEmail">
                    <Form.Control type="email" value={this.state.values.email} onChange={this.handleInputChange}/>
                    <Form.Label>نام کاربری</Form.Label>
                    <span className="form-control-icon">
                                                <svg className="bi bi-person-fill" width="20px" height="20px"
                                                     viewBox="0 0 16 16" fill="currentColor"
                                                     xmlns="http://www.w3.org/2000/svg">
                                                <path fillRule="evenodd"
                                                      d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                                                </svg>
                                            </span>
                </Form.Group>
                <Form.Group controlId="LoginPass">
                    <Form.Control type="password" value={this.state.values.password} onChange={this.handleInputChange}/>
                    <Form.Label>کلمه عبور</Form.Label>
                    <span className="form-control-icon">
                                                <svg className="bi bi-lock-fill" width="20px" height="20px"
                                                     viewBox="0 0 16 16" fill="currentColor"
                                                     xmlns="http://www.w3.org/2000/svg">
                                                  <rect width="11" height="9" x="2.5" y="7" rx="2"/>
                                                  <path fillRule="evenodd"
                                                        d="M4.5 4a3.5 3.5 0 1 1 7 0v3h-1V4a2.5 2.5 0 0 0-5 0v3h-1V4z"/>
                                                </svg>
                                            </span>
                </Form.Group>
                <Link to="/recover_password">
                    رمز عبور خود را فراموش کرده اید؟
                </Link>
                <Button type="submit" className="w-100 m-b-10">ورود</Button>
            </Form>
        );
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export default LoginForm;