import './App.css';
import Classification from './components/Classification';
import Align from './components/Alignment';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import Visualize from './components/Visualize';
import Compare from './components/Compare';


function App() {
  return (
    <Router>
            <div className="App">
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/visualize" element={<Visualize />} />
                    <Route path="/classification" element={<Classification />} />
                    <Route path="/compare" element={<Compare />} />
                    <Route path="/align" element={<Align />} />
                </Routes>
            </div>
        </Router>
  );
}

export default App;