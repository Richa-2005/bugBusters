import React, { useState } from 'react';
import axios from 'axios';
import './signup.css'; // Import the corresponding CSS file

const SignUp = () => {
  const [formData, setFormData] = useState({
    Fname: '',
    Lname: '',
    email: '',
    phoneNumber: '',
    city: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

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
    setSuccess('');

    const {  ...userData } = formData;

    try {
      
      const response = await axios.post('http://localhost:5500/user/post', userData);
      
      console.log('User registered successfully:', response.data);
      setSuccess('Registration successful! You can now sign in.');
    
      setFormData({
        Fname: '', Lname: '', email: '', phoneNumber: '', city: ''
      });
     

    } catch (err) {
      console.error('Signup error:', err.response ? err.response.data : err.message);
      if (err.response && err.response.data && err.response.data.message) {
        setError(err.response.data.message);
      } else {
        setError('Registration failed. Please try again later.');
      }
    }
  };

  return (
    <div className="signup-container">
      <form className="signup-form" onSubmit={handleSubmit}>
        <h2>Create Your Account</h2>
        <p>Join us by filling out the information below.</p>
        
        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="Fname">First Name</label>
            <input type="text" id="Fname" name="Fname" value={formData.Fname} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="Lname">Last Name</label>
            <input type="text" id="Lname" name="Lname" value={formData.Lname} onChange={handleChange} required />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input type="email" id="email" name="email" value={formData.email} onChange={handleChange} required />
        </div>

        <div className="form-group">
          <label htmlFor="phoneNumber">Phone Number</label>
          <input type="tel" id="phoneNumber" name="phoneNumber" value={formData.phoneNumber} onChange={handleChange} required />
        </div>

        <div className="form-group">
          <label htmlFor="city">City</label>
          <input type="text" id="city" name="city" value={formData.city} onChange={handleChange} required />
        </div>
        

        <button type="submit" className="submit-btn">
          Create Account
        </button>

        <div className="signin-link">
          <p>Already have an account? <a href="/signin">Sign In</a></p>
        </div>
      </form>
    </div>
  );
};

export default SignUp;