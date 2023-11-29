import React, { useState } from 'react';
import '../css/Login.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import HttpRequestUtils from './HttpRequest';

function Login({ setAuthenticated }) {

  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleEmailChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://localhost:8000', { username, password });

      if(response.data.token){
        console.log('Login successful:', response.data);
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('username', username);

        const token = localStorage.getItem('token');
        HttpRequestUtils.setToken(token);

        setAuthenticated(localStorage.getItem('token') !== null);
      }
       
    } catch (error) {
      console.error('Login error:', error);
      setError('Invalid credentials. Please try again.');
    }
  };

  const handleRegister = () =>{
    navigate('/Register');
  }

  return (
    <div className="login-container">
      <h1>Login</h1>
      {error && <div className="error-message">{error}</div>}
      <form className="login-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <label>Email</label>
          <input type="text" value={username} onChange={handleEmailChange} required />
        </div>
        <div className="input-group">
          <label>Password</label>
          <input type="password" value={password} onChange={handlePasswordChange} required />
        </div>
        <div className="buttons">
          <button className="login-button" type="submit">Login</button>
          <button className="register-button" onClick={handleRegister}>Register</button>
        </div>
      </form>
    </div>
  );
}

export default Login;
