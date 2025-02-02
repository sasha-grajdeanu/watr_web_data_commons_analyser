import './App.css'
import { Routes, Route } from 'react-router-dom'
import Home from './Home/Home'
import Navbar from './Navbar/Navbar'
import Visualize from './Visualize/Visualize'
import Compare from './Compare/Compare'

function App() {

  return (
    <>
      <div className="min-h-screen h-full">
        <Navbar/>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/visualize" element={<Visualize/>} />
            <Route path="/compare" element={<Compare/>} />
            <Route path="/classify" element={<Home/>} />
            <Route path="/align" element={<Home/>} />
          </Routes>
        </main>
      </div>
    </>
  )
}

export default App
