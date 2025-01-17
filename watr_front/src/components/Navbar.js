import React from 'react';
import { Link } from 'react-router-dom';
import "../styles/Navbar.css";
import logo from "../assets/sadsadfatcat.jpg";

const Navbar = () => {
    return(
        <nav className="navbar">
            
            <a href="/" className="logo">
                <img src={logo} alt="Logo" />
            </a>
            
            <ul className="nav-links">
                <li><Link to='/visualize'>Visualize</Link></li>
                <li><Link to="/classification">Classification</Link></li>
                <li><Link to='/compare'>Compare</Link></li>
                <li><Link to='/align'>Align</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;
