import React from 'react';
import "../styles/Navbar.css";
import logo from "../assets/sadsadfatcat.jpg";

const Navbar = () => {
    return(
        <nav className="navbar">
            
            <a href="/" className="logo">
                <img src={logo} alt="Logo" />
            </a>
            
            <ul className="nav-links">
                <li><a href='/visualize'>Visualize</a></li>
                <li><a href="/classification">Classification</a></li>
                <li><a href='/compare'>Compare</a></li>
                <li><a href='/align'>Align</a></li>
            </ul>
        </nav>
    );
}

export default Navbar;
