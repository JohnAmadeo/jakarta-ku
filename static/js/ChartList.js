import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import Request from 'superagent';
import Axios from 'axios';
import Utils from './utils';
import {Bar} from 'react-chartjs-2';

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
    var chartData = {
        labels: ["SD", "SMP", "SMA", "S1", "S2", "S3"],
        datasets: [
            {
                label: "Pendidikan",
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1,
                data: [65, 59, 80, 81, 56, 35],
                xLabels: ["Tingkat Pendidikan"]
            }
        ]
    };
    var chartOptions = {
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          ticks: {
            min: 0
          },
          scaleLabel: {
            display: true,
            labelString: 'Jumlah Orang'
          }
        }],
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Tingkat Pendidikan'
          }
        }]
      },
      tooltips: {
        callbacks: {
          label: (item) => (item.yLabel + ' Orang')
        }
      }
    };
    return (
      <div className='ChartList row'>
        <div className='col-md-6'>
          <div className='Chart'>
            <h3 style={{
              'color': '#FF8383'
            }}> 
              Jumlah Orang per Tingkat Pendidikan 
            </h3>
            <Bar data={chartData} options={chartOptions} 
                 width={600} height={250} />
          </div>
        </div>
      </div>
    )
  }
}

{/*library={{
  'tooltip': {
    'pointFormat': 'Awesome values: <b>{point.y}</b>'
  }
}*/}

module.exports = ChartList;