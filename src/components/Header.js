import React from "react";
import "./Header.css";
import { NavLink, Link } from "react-router-dom";

function Header() {
  return (
    <header>
      <div className="logo">
        <img
          src="https://i.namu.wiki/i/L7Yo035k1Na9X2BsHnGumn40P_guUPz9YWzYsM78_rFyt9PV4eXdJbyZgOJXCO4E0-yEjvT3Y2QkSkYjptTif0WqMzvOmpv5cUS6B5WRERZBKbVHy0_x-XYHUNDelaV7nX79NLrd_WIFNFprxC8xOg.svg"
          alt="덕성여대 로고"
        />
        <Link to="/" id="duksung">
          덕성여자대학교
        </Link>
      </div>
      <nav className="menu">
        <ul>
          <li>
            <NavLink
              to="/Menu/Qrcode"
              activeClassName="material-symbols-outlined"
              exact
            >
              <span class="material-symbols-outlined">qr_code_scanner</span>
            </NavLink>
          </li>
          <li>
            <NavLink to="/Menu/BasicInfo" activeClassName="active-menu" exact>
              기본 정보
            </NavLink>
          </li>
          <li>
            <NavLink to="/Menu/Status" activeClassName="active-menu" exact>
              기구별 현황
            </NavLink>
          </li>
          <li>
            <NavLink to="/Menu/Ranking" activeClassName="active-menu" exact>
              랭킹
            </NavLink>
          </li>
          <li>
            <NavLink to="/Menu/MyPage" activeClassName="active-menu" exact>
              마이페이지
            </NavLink>
          </li>
          <li className="menu-login">
            <Link to="./Login/Login">Log In ➝</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
