import express from 'express'
import dotenv from 'dotenv'
import {connectDB} from './config/db.js'
import cors from 'cors';
import getRoutes from './routes/user.routes.js'

const app = express()
dotenv.config()

app.use(express.json())
app.use(cors());

app.use('/user',getRoutes)

app.get('/',(req, res)=>{
    console.log('hello')
    res.send('Hello from the root route!');
})

const PORT = 5500 
connectDB() 

app.listen(PORT, ()=>{
    console.log(`Server started listening at port ${PORT} : http://localhost:${PORT}/`)
})