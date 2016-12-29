import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import Axios from 'axios';

import JakartaMap from './JakartaMap';
import Button from './Button';

{/* Props
  - selectedCategory (string)
    name of currently selected category

  - selectedComparison (string)
    name of currently selected comparison

  - selectedRegionList (array of strings)
    array of names of all currently selected regions
*/}
class ChartList extends React.Component {
  constructor(props) {
    super(props);
    this.renderEducation = this.renderEducation.bind(this);
    this.state = {
      chart_list: []
    }
  }
  componentWillUpdate() {
    console.log('component will update');
    Axios.post('/charts', {
      comparison: 'region',
      region_list: ['duren sawit', 'cipayung'],
      category: 'education'
    })
    .then((response) => {
      this.setState({
        chartList: response.body.chart_list
      });
    })
    .catch((err) => {console.log(error);});
  }
  renderEducation() {
    console.log('render education');
  }
  render() {
    return (
      <div>Testing API</div>
    )
  }
}

module.exports = ChartList;