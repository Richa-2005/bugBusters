import { useState } from 'react'
import NavBar from '../components/Navbar.jsx'
import {Routes, Route} from 'react-router-dom'
import SignIn from '../components/SignIn.jsx'
import HomePage from '../pages/HomePage'
import Alerts from '../pages/Alerts'
import Emergency from '../pages/Emergency'
import Awareness from '../pages/Awareness'
import SignUp from '../components/Sign-Up'


export default function App() {
  const [isSigned,setSigned] =useState(false)
  
  return (
    <>
    {!isSigned && <>
    <Routes>
      <Route path='/signup' element={<SignUp />} />
    </Routes> 
    <SignIn isSigned={isSigned} setSigned={setSigned}/>
  </>}
    {isSigned && <>

    <NavBar />
    <Routes>
      <Route path= '/' element={<HomePage />} />
      <Route path='/alerts' element ={<Alerts />} />
      <Route path= '/emergency' element={<Emergency />} />
      <Route path = '/awareness' element={<Awareness />} />
    </Routes>
    </>
}
    </>
  )
}

 
