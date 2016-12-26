import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import JakartaMap from './JakartaMap';

class Main extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className='Main'>
        <Header />
        <InfoBar />
        {/*<Display />*/}
      </div>
    )
  }
}

const Header = (props) => {
  return (
    <div className='Header'>
      <nav className="navbar navbar-fixed-top">
          <div className="navbar-header">
            <a className="navbar-brand" href="#">JakartaKu</a>
          </div>
      </nav>
    </div>
  )
}

class InfoBar extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="InfoBar">
        <div className="container">
          <CategoryList />
          <SearchBar />
        </div>
      </div>
    )
  }
}

class CategoryList extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="CategoryList">
        <button type="button" className="btn btn-lg btn-default">
          &#43; Pendidikan
        </button>
        <button type="button" className="btn btn-lg btn-default">
          &minus; Demografi
        </button>
        <button type="button" className="btn btn-lg btn-default">
          &#43; Agama
        </button>
        <button type="button" className="btn btn-lg btn-default">
          &#43; Pekerjaan
        </button>
        <button type="button" className="btn btn-lg btn-default">
          &#43; Status Pernikahan
        </button>
      </div>
    )
  }
}

class SearchBar extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    var placeholder = "Di kecamatan manakah letak lokasi ini?";
    return (
      <div className="SearchBar"> 
        <div className="input-group">
          <span className="input-group-addon" id="basic-addon1">@</span>
          <input type="text" className="form-control" 
                 placeholder={placeholder} aria-describedby="basic-addon1"/>
        </div>
      </div>  
    )
  }
}

module.exports = Main;

