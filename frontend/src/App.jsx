import { useState } from 'react'
import NavBar from '../components/Navbar.jsx'
import {Routes, Route} from 'react-router-dom'
import HomePage from '../pages/HomePage'
import Alerts from '../pages/Alerts'
import Emergency from '../pages/Emergency'
import Awareness from '../pages/Awareness'

export default function App() {

  return (
    <>
    <NavBar />
    <Routes>
      <Route path= '/' element={<HomePage />} />
      <Route path='/alerts' element ={<Alerts />} />
      <Route path= '/emergency' element={<Emergency />} />
      <Route path = '/awareness' element={<Awareness />} />
    </Routes>
    </>
  )
}

 
