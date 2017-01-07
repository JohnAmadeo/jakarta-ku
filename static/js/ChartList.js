import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import Request from 'superagent';
import Axios from 'axios';
import Utils from './utils';
import Graphic from './Graphic';

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
    this.state = {
      chartList: []
    }
  }
  componentWillMount() {
    console.log(window);
    Axios.post('/charts', {
      comparison: this.props.selectedComparison,
      region_list: this.props.selectedRegionList.length === 0 ? 
                   Utils.regionList : this.props.selectedRegionList,
      category: this.props.selectedCategory
    })
    .then((response) => {
      this.setState({
        chartList: response.data.chart_list
      });
    })
    .catch((err) => {});    
  }
  componentWillReceiveProps() {
    Axios.post('/charts', {
      comparison: this.props.selectedComparison,
      region_list: this.props.selectedRegionList.length === 0 ? 
                   Utils.regionList : this.props.selectedRegionList,
      category: this.props.selectedCategory
    })
    .then((response) => {
      console.log(response.data.chart_list)
      this.setState({
        chartList: response.data.chart_list
      });
    })
    .catch((err) => {console.log(err);});
  }
  render() {
    return (
      <div className='ChartList row'>
        <Graphic chartName={'Jumlah Orang per Status Pendidikan'}
                 chartType={'bar'}
                 dataFields={{
                   values: [10,20,30],
                   labels: ['A', 'B', 'C']   
                 }}
                 dataOptions={{
                   fieldAxisLabel: 'Nilai',
                   measureAxisLabel: 'Jumlah Orang',
                   tooltipStringFormat: ['_', 'Orang']
                 }}/>
      </div>
    )
  }
}


{/* Props 
    chartType (string)
    'bar' or 'doughnut'
    chartName (string)
    'Tingkat Pendidikan antar Kecamatan'
    dataFields (object)
    {
      values: [1,2,3],
      labels: ['a','b','c']
    }

    dataOptions (object)
    {
      fieldAxisLabel: 'Pekerjaan'
      measureAxisLabel: 'Jumlah Orang'
      tooltipStringFormat: ['NUMBER', 'Orang']
    }
*/}


module.exports = ChartList;