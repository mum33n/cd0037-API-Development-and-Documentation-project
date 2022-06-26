import React, { Component } from "react";
// import "../stylesheets/Header.css";

class Header extends Component {
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
    const pathname = window.location.pathname;
    return (
      <div className="bg-slate-900 text-white px-10 py-5 justify-between flex mb-10">
        <h1
          onClick={() => {
            this.navTo("");
          }}
          className="text-3xl text-blue-400 font-bold"
        >
          Udacitrivia
        </h1>
        <div className="flex gap-10 text-xl">
          <h2
            className={`${
              pathname === "/"
                ? "text-blue-400 hover:text-blue-300"
                : "hover:text-slate-300"
            } cursor-pointer`}
            onClick={() => {
              this.navTo("");
            }}
          >
            List
          </h2>
          <h2
            className={`${
              pathname === "/add"
                ? "text-blue-400 hover:text-blue-300"
                : "hover:text-slate-300"
            } cursor-pointer`}
            onClick={() => {
              this.navTo("/add");
            }}
          >
            Add
          </h2>
          <h2
            className={`${
              pathname === "/play"
                ? "text-blue-400 hover:text-blue-300"
                : "hover:text-slate-300"
            } cursor-pointer`}
            onClick={() => {
              this.navTo("/play");
            }}
          >
            Play
          </h2>
        </div>
      </div>
    );
  }
}

export default Header;
