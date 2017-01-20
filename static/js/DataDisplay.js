import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import Axios from 'axios';
import Utils from './utils';

import JakartaMap from './JakartaMap';
import Button from './Button';
import ChartList from './ChartList';
import LabelBar from './LabelBar';

{/* Props
  - selectedCategory (string)
    name of currently selected category

  - selectedRegionList (array of strings)
    array of names of all currently selected regions

  - language (string)
*/}
class DataDisplay extends React.Component {
  constructor(props) {
    super(props);
    this.onSelectComparison = this.onSelectComparison.bind(this);
    this.onSelectLabel = this.onSelectLabel.bind(this);
    this.getChartList = this.getChartList.bind(this);
    this.filterChart = this.filterChart.bind(this);
    this.getRegionList = this.getRegionList.bind(this);

    this.state = {
      selectedComparison: 'field',
      selectedLabelList: [],
      labelList: [],
      chartList: []
    }
  }
  onSelectComparison(comparison, event) {
    this.setState({
      selectedComparison: comparison
    })
  }
  onSelectLabel(label, event) {
    const updatedLabelList = this.state.selectedLabelList
                                       .includes(label) ? 
                             this.state.selectedLabelList
                                       .slice()
                                       .filter((currLabel) =>
                                               currLabel != label)
                             :
                             [...this.state.selectedLabelList, label];

    this.setState({
      selectedLabelList: updatedLabelList
    })
  }
  componentWillMount() {
    Axios.post('/charts', {
      comparison: this.state.selectedComparison,
      region_list: this.getRegionList(this.props, this.state),
      category: this.props.selectedCategory
    })
    .then((response) => {
      {/*console.log(response);*/}
      this.setState({
        chartList: response.data.chartList,
        labelList: this.state.selectedComparison === 'region' ? 
                   response.data.labelList : [],
        selectedLabelList: this.state.selectedComparison === 'region' ? 
                           response.data.labelList.slice(0,1) : []
      });
    })
    .catch((err) => {console.log(err);});    
  }
  componentWillUpdate(nextProps, nextState) {
    if(this.state.selectedComparison != nextState.selectedComparison || 
       this.props.selectedCategory != nextProps.selectedCategory) 
    {
      Axios.post('/charts', {
        comparison: nextState.selectedComparison,
        region_list: this.getRegionList(nextProps, nextState),
        category: nextProps.selectedCategory
      })
      .then((response) => {
        console.log(response);
        this.setState({
          chartList: response.data.chartList,
          labelList: nextState.selectedComparison === 'region' ? 
                     response.data.labelList : [],
          selectedLabelList: this.state.selectedComparison === 'region' ? 
                             response.data.labelList.slice(0,1) : []
        });
      })
      .catch((err) => {console.log(err);});
    }
    else if(this.props.selectedRegionList != nextProps.selectedRegionList) {
      Axios.post('/charts', {
        comparison: nextState.selectedComparison,
        region_list: this.getRegionList(nextProps, nextState),
        category: nextProps.selectedCategory
      })
      .then((response) => {
        console.log(response);
        this.setState({
          chartList: response.data.chartList,
          labelList: nextState.selectedComparison === 'region' ? 
                     response.data.labelList : []
        });
      })
      .catch((err) => {console.log(err);});      
    }
  }
  getChartList() {
    return this.state.selectedComparison === 'field' ?
           this.state.chartList :
           this.state.chartList.filter(this.filterChart);
  }
  filterChart(chart) {
    return this.state.selectedLabelList.includes(chart.field) 
           ? true : false;
  }
  getRegionList(currProps, currState) {
    let region_list = [];
    if(currProps.selectedRegionList.length === 0 &&
       currState.selectedComparison === 'field') 
    {
      return Utils.regionList;
    }
    else if(currProps.selectedRegionList.length < 2 &&
            currState.selectedComparison === 'region') 
    {
      return [];
    }
    else {
      region_list = currProps.selectedRegionList;
    }
    return region_list;
  }
  render() {
    return (
      <div className="DataDisplay">
        <div className="container">
          <ComparisonBar 
            onSelectComparison={this.onSelectComparison}
            selectedComparison={this.state.selectedComparison} 
            selectedRegionList={this.props.selectedRegionList}
            language={this.props.language}/>
          {this.state.selectedComparison === 'region' ? 
           (<LabelBar 
             onSelectLabel={this.onSelectLabel}
             selectedLabelList={this.state.selectedLabelList}
             labelList={this.state.labelList}/>)
           :
           null
          }
          <ChartList 
            selectedCategory={this.props.selectedCategory}
            selectedComparison={this.state.selectedComparison}
            selectedRegionList={this.props.selectedRegionList}
            chartList={this.getChartList()}/>
        </div>
      </div>
    )
  }
}

DataDisplay.propTypes = {
  selectedComparison: React.PropTypes.oneOf(["field", "region"])
}

{/* Props
  - onSelectComparison (function)
    event handler function that updates the state of the 
    currently selected comparison

  - selectedComparison (string)
    name of currently selected comparison
*/}
class ComparisonBar extends React.Component {
  constructor(props) {
    super(props);
    this.isComparisonSelected = this.isComparisonSelected.bind(this);
    this.isComparisonHoveredOver = this.isComparisonHoveredOver.bind(this);
    this.onHoverOnComparison = this.onHoverOnComparison.bind(this);
    this.state = ({
      hoveredComparison: ''
    })
  }
  isComparisonSelected(comparison) {
    return this.props.selectedComparison === comparison;
  }
  isComparisonHoveredOver(comparison) {
    return this.state.hoveredComparison === comparison
  }
  onHoverOnComparison(comparison, event) {
    if(event.type === 'mouseout') {
      this.setState({
        hoveredComparison: ''
      })
    }
    else if(event.type === 'mouseover') {
      this.setState({
        hoveredComparison: comparison
      })
    }
  }
  render() {
    return (
      <div className="ComparisonBar">
        <Button 
          key={1} 
          text={this.props.language === 'english' ? 
                'Compare by Field' : 'Bandingkan bidang'} 
          isSelected={this.isComparisonSelected("field")}
          onButtonClick={this.props.onSelectComparison
                                   .bind(this, "field")}
          isHoveredOver={this.isComparisonHoveredOver('field')}
          onHover={this.onHoverOnComparison.bind(this, 'field')} 
          colorScheme={'red'} />
        {this.props.selectedRegionList.length < 2 ?
         null 
         : 
         (<Button 
            key={2} 
            text={this.props.language === 'english' ? 
                  'Compare by Region' : 'Bandingkan kecamatan'}
            isSelected={this.isComparisonSelected("region")}
            onButtonClick={this.props.onSelectComparison
                                     .bind(this, "region")}
            isHoveredOver={this.isComparisonHoveredOver('region')}
            onHover={this.onHoverOnComparison.bind(this, 'region')} 
            colorScheme={'red'} />)
        }
      </div>
    )
  }
}

module.exports = DataDisplay;
  