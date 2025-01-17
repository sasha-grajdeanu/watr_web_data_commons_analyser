import './App.css';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import Classification from './components/Classification';


const Home = () => <div className='body'><h1>Welcome to the Dashboard</h1></div>
const Visualize = () => <div className="body"><h1>Visualize Data</h1></div>;
const Compare = () => <div className="body"><h1>Comparison Page</h1></div>;
const Align = () => <div className="body"><h1>Alignment Page</h1></div>;



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
