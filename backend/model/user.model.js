import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
  Fname: {
    type: String,
    required: true,
    unique: true,
    trim: true,
  },
  Lname: {
    type: String,
    required: true,
    unique: true,
    trim: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true,
  },
  phoneNumber:{
    type:Number,
    required: true,
    unique: true,
  },
  city :{
    type : String,
    required: true
  }
}, {
  timestamps: true
});

const User = mongoose.model('User', userSchema);
export default User