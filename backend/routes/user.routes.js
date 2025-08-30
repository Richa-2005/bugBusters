import express from 'express'
import { registerUser,getUser } from '../controllers/user.controller.js';
const router = express.Router()

router.post('/post',registerUser)
router.get('/get',getUser)

export default router;