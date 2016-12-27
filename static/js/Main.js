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
        <Display />
        {/*<ChartList />*/}
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
          &#43; Pernikahan
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

class Display extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="Display">
        <div className="box col-md-6">
          <RegionList />
        </div>
        <div className="box col-md-6">
          <JakartaMap />
        </div>
      </div>
    )
  }
}

class RegionList extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    var regionList = ['Cakung','Cempaka Putih','Cengkareng','Cilandak','Cilincing','Cipayung','Ciracas','Duren Sawit','Gambir','Grogol Petamburan','Jagakarsa','Jatinegara','Johar Baru','Kali Deres','Kebayoran Baru','Kebayoran Lama','Kebon Jeruk','Kelapa Gading','Kemayoran','Kembangan','Koja','Kramat Jati','Makasar','Mampang Prapatan','Matraman','Menteng','Pademangan','Palmerah','Pancoran','Pasar Minggu','Pasar Rebo','Penjaringan','Pesanggrahan','Pulo Gadung','Sawah Besar','Senen','Setia Budi','Taman Sari','Tambora','Tanah Abang','Tanjung Priok','Tebet'];
    return (
      <div className="RegionList"> 
        {regionList.map((region) => (
          <Region name={region} />
        ))}
      </div>
    )
  }
}

class Region extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <button type="button" className="btn btn-lg btn-default">
        &#43; {this.props.name}
      </button>
    )
  }
}

module.exports = Main;

{/*
<div className="dropdown">
  <button className="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
    Dropdown &nbsp;
    <span className="caret"></span>
  </button>
  <ul className="dropdown-menu" aria-labelledby="dropdownMenu1">
    <li><a href="#">Action</a></li>
    <li><a href="#">Another action</a></li>
    <li><a href="#">Something else here</a></li>
    <li role="separator" class="divider"></li>
    <li><a href="#">Separated link</a></li>
  </ul>
</div>
*/}
