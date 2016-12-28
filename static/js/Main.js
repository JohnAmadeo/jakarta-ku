import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import JakartaMap from './JakartaMap';

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      category: "education",
      searchText: "",
      selectedRegions: [],
      selectedComparison: "region"
    }
  }
  render() {
    return (
      <div className='Main'>
        <Header />
        <CategoryBar category={this.state.category}/>
        <MapDisplay />
        <DataDisplay />
      </div>
    )
  }
}

{/*Main.propTypes = {
  category: React.PropTypes.string.isRequired,
  searchText: React.PropTypes.string.isRequired,
  selectedRegions: React.PropTypes.arrayOf(React.PropTypes.string).isRequired,
  selectedComparison: React.PropTypes.oneOf(["education", "region"]).isRequired  
}*/}

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

class CategoryBar extends React.Component {
  constructor(props) {
    super(props);

    this.indoToEnglish = this.indoToEnglish.bind(this);
    this.renderButtonSymbol = this.renderButtonSymbol.bind(this);
    this.renderButtonList = this.renderButtonList.bind(this);
  }
  renderButtonList() {
    const categoryListInIndo = ['pendidikan', 'demografi', 'agama',
                                'pekerjaan', 'pernikahan'];
    return categoryListInIndo.map((categoryInIndo, index) => {
      const category = this.indoToEnglish(categoryInIndo);
      return (
        <button type="button" className="btn btn-lg btn-default"
                onClick={this.props.onSelectCategory} key={index}>
          {this.renderButtonSymbol(category)} 
          {categoryInIndo[0].toUpperCase() + categoryInIndo.substr(1)}
        </button>
      )
    });
  }
  renderButtonSymbol(categoryInIndo) {
    console.log(categoryInIndo);
    if(this.props.category === categoryInIndo) {
      return (<span>&minus; &nbsp;</span>);
    }
    else return (<span>&#43; &nbsp;</span>);
  }
  indoToEnglish(categoryInIndo) {
    const translation = {
      pendidikan: 'education',
      demografi: 'demographics',
      agama: 'religion',
      pekerjaan: 'occupation',
      pernikahan: 'marriage'
    }
    return translation[categoryInIndo];
  }
  render() {
    return (
      <div className="CategoryBar">
        {this.renderButtonList()}
      </div>
    )
  } 
}

class SearchBar extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const placeholder = "Pilih kecamatan dimana lokasi ini terletak";
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

class MapDisplay extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="MapDisplay row">
        <div className="col-md-6">
          <SearchBar />
          <RegionList />
        </div>
        <div className="col-md-6">
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
    const regionList = ['Cakung','Cempaka Putih','Cengkareng','Cilandak','Cilincing','Cipayung','Ciracas','Duren Sawit','Gambir','Grogol Petamburan','Jagakarsa','Jatinegara','Johar Baru','Kali Deres','Kebayoran Baru','Kebayoran Lama','Kebon Jeruk','Kelapa Gading','Kemayoran','Kembangan','Koja','Kramat Jati','Makasar','Mampang Prapatan','Matraman','Menteng','Pademangan','Palmerah','Pancoran','Pasar Minggu','Pasar Rebo','Penjaringan','Pesanggrahan','Pulo Gadung','Sawah Besar','Senen','Setia Budi','Taman Sari','Tambora','Tanah Abang','Tanjung Priok','Tebet'];
    return (
      <div className="RegionList"> 
        {regionList.map((region, index) => (
          <Region name={region} key={index}/>
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

class DataDisplay extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="DataDisplay">
        <div className="container">
          <ComparisonBar />
          <LoremIpsum />
          {/*<ChartList />*/}
        </div>
      </div>
    )
  }
}

class ComparisonBar extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="ComparisonBar">
        <button type="button" className="btn btn-lg btn-default">
          &#43; Bandingkan kategori
        </button>
        <button type="button" className="btn btn-lg btn-default">
          &minus; Bandingkan kecamatan
        </button>
      </div>
    )
  }
}

const LoremIpsum = (props) => {
  return (
    <p>
      "It is a period of civil war. Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire.
      During the battle, Rebel spies managed to steal secret plans to the Empire's ultimate weapon, the DEATH STAR, an armored space station with enough power to destroy an entire planet.
      Pursued by the Empire's sinister agents, Princess Leia races home aboard her starship, custodian of the stolen plans that can save her people and restore freedom to the galaxy....
    </p>
  )
}

module.exports = Main;
