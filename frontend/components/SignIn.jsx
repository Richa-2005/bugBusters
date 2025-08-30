import React, { useState } from 'react';
import axios from 'axios';
// Import useNavigate for programmatic navigation
import { Link, useNavigate } from 'react-router-dom';
import './signin.css'; 

const SignIn = (props) => {
  // Initialize the navigate function
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: '',
    phoneNumber: '',
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); 
    setError(''); 

    try {
      // This GET request checks if a user with this email AND phone number exists.
      const response = await axios.get('http://localhost:5500/user/get', {
        params: formData, // Sends email and phoneNumber as query params
      });

      
      if(response.status === 200){
       
        props.setSigned(true);
        navigate('/');
      }

    } catch (err) {
      // An error (like a 404 Not Found) from the backend will be caught here.
      console.error('Sign-in error:', err);
      if (err.response && err.response.status === 404) {
        setError('User not found. Please check your credentials or sign up.');
      } else {
        setError('Failed to sign in. An unexpected error occurred.');
      }
    }
  };

  return (
    <div className="signin-container">
      <form className="signin-form" onSubmit={handleSubmit}>
        <h2>Sign In</h2>
        <p>Enter your details to access your account.</p>

        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="you@example.com"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="phoneNumber">Phone Number</label>
          <input
            type="tel" 
            id="phoneNumber"
            name="phoneNumber"
            value={formData.phoneNumber}
            onChange={handleChange}
            placeholder="123-456-7890"
            required
          />
        </div>
        
        {error && <p className="error-message">{error}</p>}
        
        
        <button type="submit" className="submit-btn">
          Sign In
        </button>

        <div className="signup-link">
          <p>Don't have an account? <Link to={'/signup'}>Sign Up</Link></p>
        </div>
      </form>
    </div>
  );
};

export default SignIn;
