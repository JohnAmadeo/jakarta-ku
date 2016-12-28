import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import JakartaMap from './JakartaMap';
import Button from './Button';

{/* Props 
  - selectedRegionList (array of strings)
    array of regions that are currently selected

  - onSelectRegion (function)
    event handler that updates the state of 
    regions that are currently selected  
*/}

class MapDisplay extends React.Component {
  constructor(props) {
    super(props);
    this.isRegionSelected = this.isRegionSelected.bind(this);
  }
  isRegionSelected(region) {
    return this.props.selectedRegionList.includes(region);
  }
  render() {
    return (
      <div className="MapDisplay row">
        <div className="col-md-6">
          <SearchBar />
          <RegionList onSelectRegion={this.props.onSelectRegion}
                      isRegionSelected={this.isRegionSelected}/>
        </div>
        <div className="col-md-6">
          <JakartaMap onSelectRegion={this.props.onSelectRegion} 
                      isRegionSelected={this.isRegionSelected}/>
        </div>        
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

{/* Props
  - isRegionSelected (function)
    checking function that returns true if the region
    of the component is selected; false otherwise

  - onSelectRegion (function)
    event handler that updates the state of 
    regions that are currently selected 
*/}

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

{/* Props
  - isRegionSelected (function)
    checking function that returns true if the region
    of the component is selected; false otherwise

  - onSelectRegion (function)
    event handler that updates the state of 
    regions that are currently selected 

  - region (string)
    name of region
*/}

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
      <Button 
        onButtonClick={this.props.onSelectRegion
                                 .bind(this, this.props.region)} 
        key={this.props.key}
        selected={this.props.isRegionSelected(this.props.region)}
        text={this.capitalizeName(this.props.region)} />
    )
  }
}

module.exports = MapDisplay;
