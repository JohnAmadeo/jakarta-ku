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
          <div>
            {/*<Searchbar />*/}
            asdf
          </div>
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
          &#43; Education
        </button>
        <button type="button" className="btn btn-lg btn-default">
          &minus; Demographics
        </button>
        <button type="button" className="btn btn-lg btn-default">
          &#43; Religion
        </button>
        <button type="button" className="btn btn-lg btn-default">
          &#43; Occupation
        </button>
        <button type="button" className="btn btn-lg btn-default">
          &#43; Marriage
        </button>
      </div>
    )
  }
}

module.exports = Main;