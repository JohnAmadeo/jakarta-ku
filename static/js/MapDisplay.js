import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import Utils from './utils';

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
    this.isRegionHoveredOver = this.isRegionHoveredOver.bind(this);
    this.onHoverOnRegion = this.onHoverOnRegion.bind(this);

    this.state = {
      hoveredRegionList: []
    }
  }
  isRegionSelected(region) {
    return this.props.selectedRegionList.includes(region);
  }
  isRegionHoveredOver(region) {
    return this.state.hoveredRegionList.includes(region);
  }
  onHoverOnRegion(region, event) {
    const hoveredRegionList = this.state.hoveredRegionList;
    this.setState({
      hoveredRegionList: 
        hoveredRegionList.includes(region) ?
        hoveredRegionList.slice()
                         .filter((currRegion) => currRegion != region) :
        [...hoveredRegionList, region]
    });
  }
  render() {
    return (
      <div className="MapDisplay row">
        <div className="col-md-6">
          {/*<SearchBar />*/}
          <RegionList onSelectRegion={this.props.onSelectRegion}
                      isRegionSelected={this.isRegionSelected}
                      onHoverOnRegion={this.onHoverOnRegion}
                      isRegionHoveredOver={this.isRegionHoveredOver}/>
        </div>
        <div className="col-md-6">
          <JakartaMap onSelectRegion={this.props.onSelectRegion} 
                      isRegionSelected={this.isRegionSelected}
                      onHoverOnRegion={this.onHoverOnRegion}
                      isRegionHoveredOver={this.isRegionHoveredOver}/>
        </div>        
      </div>
    )
  }
}

MapDisplay.propTypes = {
  hoveredRegionList: React.PropTypes.arrayOf(React.PropTypes.string)
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

  - isRegionHoveredOver (function)
    checking function returns true if region
    is hovered over; false otherwise

  - onHoverOnRegion (function)
    event handler that updates state of regions currently
    being hovered over
*/}

class RegionList extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="RegionList"> 
        {Utils.regionList.map((region, index) => (
          <Region region={region} key={index}
                  onSelectRegion={this.props.onSelectRegion}
                  isRegionSelected={this.props.isRegionSelected}
                  onHoverOnRegion={this.props.onHoverOnRegion}
                  isRegionHoveredOver={this.props.isRegionHoveredOver}
                  />
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

  - isRegionHoveredOver (function)
    checking function returns true if region
    is hovered over; false otherwise

  - onHoverOnRegion (function)
    event handler that updates state of regions currently
    being hovered over

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
        onHover={this.props.onHoverOnRegion
                            .bind(this, this.props.region)}
        key={this.props.key}
        isSelected={this.props.isRegionSelected(this.props.region)}
        isHoveredOver={this.props.isRegionHoveredOver(this.props.region)}
        text={this.capitalizeName(this.props.region)} 
        colorScheme={'red'}/>
    )
  }
}

module.exports = MapDisplay;
