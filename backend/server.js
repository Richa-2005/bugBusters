import dotenv from 'dotenv';
import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors'; // 1. CORS is needed for frontend communication

dotenv.config();

const app = express();

// --- 1. Mongoose Schema and Model (Defining the structure of user data) ---
// This schema matches the fields from your registration form.
const userSchema = new mongoose.Schema({
    firstName: { type: String, required: true },
    lastName: { type: String, required: true },
    email: { type: String, required: true, unique: true }, // unique ensures no duplicate emails
    phoneNumber: { type: String, required: true },
    city: { type: String, required: true },
    // NOTE: For a real sign-up, you would add a 'password' field here 
    // and use bcrypt to hash and store it securely.
}, { timestamps: true });

const User = mongoose.model('User', userSchema);

// Middleware
app.use(express.json()); // Allows the server to read JSON data sent from the frontend
app.use(cors());         // Allows your frontend (e.g., on port 3000/5173) to talk to the backend (on port 5000)

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI)
.then(() => console.log("✅ MongoDB connected"))
.catch((err) => console.error("❌ DB connection error:", err));

// --- 2. Routes ---

// Simple testing route
app.get('/', (req, res) => {
    res.send("API is running...");
});

// New Registration Route: Handles the "Create Account" request from the frontend
app.post('/api/register', async (req, res) => {
    try {
        // Destructure data sent in the request body
        const { firstName, lastName, email, phoneNumber, city } = req.body;

        // Simple check to ensure required data is present
        if (!email || !firstName) {
            return res.status(400).json({ message: 'Missing required fields (email and first name).' });
        }

        // Create a new user document instance
        const newUser = new User({
            firstName,
            lastName,
            email,
            phoneNumber,
            city
        });

        // Save the user to the database
        await newUser.save();

        // Respond with success and the new user ID
        res.status(201).json({ 
            message: 'User registered successfully!',
            userId: newUser._id
        });

    } catch (error) {
        console.error('Registration Error:', error);
        
        // Error code 11000 means a duplicate key was found (in this case, the email)
        if (error.code === 11000) {
            return res.status(409).json({ message: 'Email address already in use.' });
        }
        
        // Generic server error response
        res.status(500).json({ message: 'Registration failed. Please try again later.' });
    }
});
