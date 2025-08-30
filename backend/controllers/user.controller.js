import mongoose from 'mongoose'
import User from '../model/user.model.js'

const registerUser = async (req, res) => {
    try {
      const { Fname, Lname, email, phoneNumber, city } = req.body;

      if (!Fname || !Lname || !email || !phoneNumber || !city) {
        return res.status(400).json({ message: 'Please enter all fields.' });
      }
      const userExists = await User.findOne({
        $or: [{ email }, { phoneNumber }],
      });
  
      if (userExists) {
        return res.status(400).json({ message: 'User already exists with this email or phone number.' });
      }
  
      const newUser = await User.create({
        Fname,
        Lname,
        email,
        phoneNumber,
        city,
      });
  
      if (newUser) {
        res.status(201).json({
          message: 'User registered successfully',
          _id: newUser._id,
          Fname: newUser.Fname,
          Lname: newUser.Lname,
          email: newUser.email,
          phoneNumber: newUser.phoneNumber,
          city: newUser.city,
        });
      } else {
        res.status(400).json({ message: 'Invalid user data' });
      }
    } catch (error) {
      res.status(500).json({ message: 'Server error', error: error.message });
    }
  };
  const getUser = async (req, res) => {
    try {
      
      const { email, phoneNumber } = req.query;
  
      if (!email || !phoneNumber) {
        return res.status(400).json({ message: 'Email and phone number are required.' });
        
      }

      const user = await User.findOne({ email, phoneNumber });
      if (!user) {
        return res.status(404).json({ message: 'Invalid credentials. User not found.' });
        
      }
      res.status(200).json({
        message: 'Sign-in successful!',
        user: {
          id: user._id,
          Fname: user.Fname,
          Lname: user.Lname,
          email: user.email,
          city: user.city,
        },
      });
  
    } catch (error) {
      console.error("Error during user sign-in:", error);
      res.status(500).json({ message: 'Internal server error. Please try again later.' });
    }
  };
  
  export { registerUser,getUser };

