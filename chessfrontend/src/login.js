import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ setAuthToken }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();

    const loginData = {
      username,
      password,
    };

    try {
      const response = await axios.post('http://localhost:8000/login/', loginData);
      // Assuming the response contains an access token
      const { access_token } = response.data;
      localStorage.setItem('authToken', access_token);
      setAuthToken(access_token); // Store the access token in state
      setMessage('Login successful!');
      setError('');
    } catch (err) {
      setMessage('');
      setError('Invalid credentials. Please try again.');
    }
  };
  var autht=localStorage.getItem('authToken');
  console.log("Auth Token:", autht);

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {message && <p style={{ color: 'green' }}>{message}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;