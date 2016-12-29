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
    const newselectedRegionList 
      = this.state.selectedRegionList.includes(region) ?
        this.state.selectedRegionList
          .slice()
          .filter((currRegion) => currRegion != region) :
        [...this.state.selectedRegionList, region];

    this.setState({
      selectedRegionList: newselectedRegionList
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
  }
  isCategorySelected(category) {
    return this.props.selectedCategory === category;
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
          key={index}
          selected={this.isCategorySelected(category)}
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

module.exports = Main;
