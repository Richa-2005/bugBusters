import { useState } from 'react'
import NavBar from '../components/Navbar'
import {Routes, Route} from 'react-router-dom'
import HomePage from '../pages/homePage'
import Alerts from '../pages/Alerts'
import Emergency from '../pagesEmergency'
import Awareness from '../pages/Awareness'

export default function App() {

  return (
    <>
    <NavBar />
    <Routes>
      <Route path= '/' element={<HomePage />} />
      <Route path='/alerts' element ={<Alerts />} />
      <Route path= '/activity' element={<Emergency />} />
      <Route path = '/account' element={<Awareness />} />
    </Routes>
    </>
  )
}

 
