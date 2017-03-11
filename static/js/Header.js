import React from 'react';
import ReactDOM from 'react-dom';

{/* Props
  - N/A
*/}
const Header = (props) => {
  console.log();
  return (
    <div className='Header'>
      <nav className="navbar navbar-fixed-top">
          <div className="navbar-header">
            <ul className="FlagBar nav navbar-nav navbar-right"> 
              <span className='AppName'> JakartaKu</span>
            </ul>
          </div>
          <div id="navbar" className="navbar-collapse collapse">
            <ul className="Credit nav navbar-nav navbar-right">
              <li>
                <a href="http://github.com/johnamadeo">
                  Made by John Amadeo,</a>
              </li>
              <li>
                <a href="http://data.jakarta.go.id/">
                  Data from Jakarta OpenData                 
                </a>
              </li>
            </ul>
          </div>
      </nav>
    </div>
  )
}

module.exports = Header;
