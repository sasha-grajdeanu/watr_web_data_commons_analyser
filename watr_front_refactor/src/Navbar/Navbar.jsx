import { NavLink, useLocation } from "react-router-dom";
import logo from "../assets/sadsadfatcat.jpg";
import { AiOutlineClose, AiOutlineMenu } from "react-icons/ai";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [nav, setNav] = useState(false);
  const location = useLocation();
  const navItems = [
    { label: "Visualization", path: "/visualize" },
    { label: "Comparison", path: "/compare" },
    { label: "Classification", path: "/classify" },
    { label: "Alignment", path: "/align" },
  ];

  const handleScroll = () => {
    if (nav) {
      setNav(false);
    }
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [nav]);

  const handleNav = () => {
    setNav(!nav);
  };

  const resetNav = () => {
    setNav(false);
  };

  return (
    <div className="bg-watr-100 flex justify-between items-center h-16 px-4 text-white font-montserrat">
      <NavLink to="/" className="text-2xl flex items-center">
        <h1>WATR</h1>
      </NavLink>
      <div className="hidden md:flex">
        {navItems.map((item, index) => (
          <NavLink
            key={index}
            to={item.path}
            className={`p-2 hover:bg-watr-200 rounded-xl m-1 duration-300 text-lg ${
              location.pathname === item.path
                ? "bg-watr-200 duration-300"
                : "cursor-pointer"
            }`}
          >
            {item.label}
          </NavLink>
        ))}
      </div>
      <div onClick={handleNav} className="block md:hidden">
        {nav ? (
          <AiOutlineClose size={20} className="cursor-pointer" />
        ) : (
          <AiOutlineMenu size={20} className="cursor-pointer" />
        )}
      </div>
      <div
        className={
          nav
            ? "fixed md:hidden left-0 top-[64px] w-[100%] bg-watr-100 ease-in-out duration-0 flex flex-col text-lg border-y-2 border-watr-200"
            : "ease-in-out hidden w-[60%] duration-0 fixed top-0 bottom-0 left-[-100%] text-lg"
        }
      >
        {navItems.map((item, index) => (
          <NavLink
            key={index}
            to={item.path}
            className={`p-4 hover:bg-watr-200 w-full text-center duration-300 ${
              location.pathname === item.path
                ? "bg-watr-200 duration-300"
                : "cursor-pointer"
            }`}
            onClick={resetNav}
          >
            {item.label}
          </NavLink>
        ))}
      </div>
    </div>
  );
}
