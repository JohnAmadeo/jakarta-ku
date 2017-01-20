import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import Utils from './utils';

import MapDisplay from './MapDisplay';
import DataDisplay from './DataDisplay';
import Button from './Button';


class Main extends React.Component {
  constructor(props) {
    super(props);
    this.onSelectCategory = this.onSelectCategory.bind(this);
    this.onSelectRegion = this.onSelectRegion.bind(this);

    this.state = {
      selectedCategory: "education",
      searchText: "",
      selectedRegionList: []
    }
  }
  onSelectCategory(category, event) {
    this.setState({
      selectedCategory: category
    });
  }
  onSelectRegion(region, event) {
    const newSelectedRegionList 
      = this.state.selectedRegionList.includes(region) ?
        this.state.selectedRegionList
          .slice()
          .filter((currRegion) => currRegion != region) :
        [...this.state.selectedRegionList, region];

    this.setState({
      selectedRegionList: newSelectedRegionList
    })
  }
  render() {
    return (
      <div className='Main'>
        <Header />
        <CategoryBar onSelectCategory={this.onSelectCategory}
                     selectedCategory={this.state.selectedCategory}/>

        <MapDisplay 
          onSelectRegion={this.onSelectRegion}
          selectedRegionList = {this.state.selectedRegionList}/>

        <DataDisplay 
          selectedCategory={this.state.selectedCategory}
          selectedRegionList = {this.state.selectedRegionList}/>
      </div>
    )
  }
}

Main.propTypes = {
  selectedCategory: React.PropTypes.oneOf(["education", "demographics",
                                            "religion", "occupation", 
                                            "marriage"]),
  searchText: React.PropTypes.string,
  selectedRegionList: React.PropTypes.arrayOf(React.PropTypes.string)
}

{/* Props
  - N/A
*/}
const Header = (props) => {
  return (
    <div className='Header'>
      <nav className="navbar navbar-fixed-top">
          <div className="navbar-header">
            <a className="navbar-brand" href="#">JakartaKu</a>
          </div>
          <div id="navbar" className="navbar-collapse collapse">
            <ul className="nav navbar-nav navbar-right">
              <li><a href="http://github.com/johnamadeo">Made w/ love by John Amadeo</a></li>
            </ul>
          </div>
      </nav>
    </div>
  )
}

{/* Props
  - onSelectCategory (function)
    event handler function that updates the state of the
    currently selected category

  - selectedCategory (string)
    name of currently selected category
*/}
class CategoryBar extends React.Component {
  constructor(props) {
    super(props);
    this.renderButtonList = this.renderButtonList.bind(this);
    this.isCategorySelected = this.isCategorySelected.bind(this);
    this.isCategoryHoveredOver = this.isCategoryHoveredOver.bind(this);
    this.onHoverOnCategory = this.onHoverOnCategory.bind(this);

    this.state = {
      hoveredCategory: '',
    }
  }
  isCategorySelected(category) {
    return this.props.selectedCategory === category;
  }
  isCategoryHoveredOver(category) {
    return this.state.hoveredCategory === category;
  }
  onHoverOnCategory(category, event) {
    if(event.type === 'mouseout') {
      this.setState({
        hoveredCategory: ''
      })
    }
    else if(event.type === 'mouseover') {
      this.setState({
        hoveredCategory: category
      })
    }
  }
  renderButtonList() {
    const categoryListInIndo = ['pendidikan', 'demografi', 'agama',
                                'pekerjaan', 'pernikahan'];
    return categoryListInIndo.map((categoryInIndo, index) => {
      const category = Utils.translate(categoryInIndo);
      return (
        <Button 
          onButtonClick={this.props.onSelectCategory
                                   .bind(this, category)}
          onHover={this.onHoverOnCategory.bind(this, category)}
          key={index}
          isSelected={this.isCategorySelected(category)}
          isHoveredOver={this.isCategoryHoveredOver(category)}
          text={categoryInIndo[0].toUpperCase() + 
                categoryInIndo.substr(1)} 
          colorScheme={'blue'} />
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

CategoryBar.propTypes = {
  hoveredCategory: React.PropTypes.string
}

module.exports = Main;
