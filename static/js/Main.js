import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import JakartaMap from './JakartaMap';
import Translator from './translator';
import ButtonPlus from './ButtonPlus';

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.isCategorySelected = this.isCategorySelected.bind(this);
    this.isRegionSelected = this.isRegionSelected.bind(this);
    this.onSelectCategory = this.onSelectCategory.bind(this);
    this.onSelectRegion = this.onSelectRegion.bind(this);

    this.state = {
      category: "education",
      searchText: "",
      selectedRegions: [],
      selectedComparison: "region"
    }
  }
  isCategorySelected(category) {
    return this.state.category === category;
  }
  isRegionSelected(region) {
    return this.state.selectedRegions.includes(region);
  }
  onSelectCategory(category, event) {
    this.setState({
      category: category
    });
  }
  onSelectRegion(region, event) {
    const newSelectedRegions 
      = this.state.selectedRegions.includes(region) ?
        this.state.selectedRegions
          .slice()
          .filter((currRegion) => currRegion != region) :
        [...this.state.selectedRegions, region];

    this.setState({
      selectedRegions: newSelectedRegions
    })
  }
  render() {
    return (
      <div className='Main'>
        <Header />
        <CategoryBar onSelectCategory={this.onSelectCategory}
                     isCategorySelected={this.isCategorySelected} />
        <MapDisplay onSelectRegion={this.onSelectRegion}
                    isRegionSelected={this.isRegionSelected}/>
        <DataDisplay />
      </div>
    )
  }
}

Main.propTypes = {
  category: React.PropTypes.string,
  searchText: React.PropTypes.string,
  selectedRegions: React.PropTypes.arrayOf(React.PropTypes.string),
  selectedComparison: React.PropTypes.oneOf(["education", "region"])
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

class CategoryBar extends React.Component {
  constructor(props) {
    super(props);
    this.renderButtonList = this.renderButtonList.bind(this);
  }
  renderButtonList() {
    const categoryListInIndo = ['pendidikan', 'demografi', 'agama',
                                'pekerjaan', 'pernikahan'];
    return categoryListInIndo.map((categoryInIndo, index) => {
      const category = Translator.indoToEnglish(categoryInIndo);
      return (
        <ButtonPlus 
          onButtonClick={this.props.onSelectCategory
                                   .bind(this, category)}
          key={category}
          isSelected={this.props.isCategorySelected(category)}
          text={categoryInIndo[0].toUpperCase() + 
                categoryInIndo.substr(1)} />
      )
    });
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
          <RegionList onSelectRegion={this.props.onSelectRegion}
                      isRegionSelected={this.props.isRegionSelected}/>
        </div>
        <div className="col-md-6">
          <JakartaMap isRegionSelected={this.props.isRegionSelected}/>
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
    const regionList = ['cakung', 'cempaka putih', 'cengkareng', 'cilandak', 'cilincing', 'cipayung', 'ciracas', 'duren sawit', 'gambir', 'grogol petamburan', 'jagakarsa', 'jatinegara', 'johar baru', 'kalideres', 'kebayoran baru', 'kebayoran lama', 'kebon jeruk', 'kelapa gading', 'kemayoran', 'kembangan', 'koja', 'kramat jati', 'makasar', 'mampang prapatan', 'matraman', 'menteng', 'pademangan', 'palmerah', 'pancoran', 'pasar minggu', 'pasar rebo', 'penjaringan', 'pesanggrahan', 'pulo gadung', 'sawah besar', 'senen', 'setiabudi', 'taman sari', 'tambora', 'tanah abang', 'tanjung priok', 'tebet'];
    return (
      <div className="RegionList"> 
        {regionList.map((region, index) => (
          <Region region={region} key={index}
                  onSelectRegion={this.props.onSelectRegion}
                  isRegionSelected={this.props.isRegionSelected}/>
        ))}
      </div>
    )
  }
}

class Region extends React.Component {
  constructor(props) {
    super(props);
    this.capitalizeName = this.capitalizeName.bind(this);
  }
  capitalizeName(name) {
    return name.split(' ')
               .map((word) => word[0].toUpperCase() + word.substr(1))
               .join(' ');
  }
  render() {
    return (
      <ButtonPlus 
        onButtonClick={this.props.onSelectRegion
                                 .bind(this, this.props.region)} 
        key={this.props.key}
        isSelected={this.props.isRegionSelected(this.props.region)}
        text={this.capitalizeName(this.props.region)} />
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
