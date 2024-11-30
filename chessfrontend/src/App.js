import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Register from './register';
import Login from './login';

const App = () => {
  const [authToken, setAuthToken] = useState(null);

  const setToken = (token) => {
    setAuthToken(token);
    localStorage.setItem('authToken', token); // Optionally store token in local storage
  };

  return (
    <Router>
      <div>
        <h1>Chess Game App</h1>

        {!authToken ? (
          <div>
            <h2>Please log in or register</h2>
            {/* Navigation links to Login and Register */}
            <nav>
              <ul>
                <li>
                  <Link to="/login">Login</Link>
                </li>
                <li>
                  <Link to="/register">Register</Link>
                </li>
              </ul>
            </nav>
            <Routes>
              <Route path="/register" element={<Register />} />
              <Route path="/login" element={<Login setAuthToken={setToken} />} />
            </Routes>
          </div>
        ) : (
          <div>
            <h2>Welcome! You are logged in.</h2>
            {/* Render logged-in user features here */}
          </div>
        )}
      </div>
    </Router>
  );
};

export default App;