import express from 'express'
import dotenv from 'dotenv'
import {connectDB} from './config/db.js'
import cors from 'cors';
//import routes

const app = express()
dotenv.config()

app.use(express.json())
app.use(cors());

//routes
app.use()
app.use()


app.get('/',(req, res)=>{
    console.log('hello')
    res.send('Hello from the root route!');
})

const PORT = 5500 //or import from .env file
connectDB() 

app.listen(PORT, ()=>{
    console.log(`Server started listening at port ${PORT} : http://localhost:${PORT}/`)
})