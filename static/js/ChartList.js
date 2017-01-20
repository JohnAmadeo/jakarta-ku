import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import Axios from 'axios';
import Utils from './utils';

import Graphic from './Graphic';
import {TestBarList, TestDoughnutList} from './TestCharts';
import LabelBar from './LabelBar';

{/* Props
  - selectedCategory (string)
    name of currently selected category

  - selectedComparison (string)
    name of currently selected comparison

  - selectedRegionList (array of strings)
    array of names of all currently selected regions

  - chartList (array of objects)
*/}
class ChartList extends React.Component {
  constructor(props) {
    super(props);
    this.getPalette = this.getPalette.bind(this);
  }
  getPalette(chart) {
    if(this.props.selectedComparison === 'field') {
      return Utils.getPalette(chart.dataFields.values.length,
                              Utils.palette.backgroundColors[0])
    }
    else if(this.props.selectedComparison === 'region') {
      if(chart.chartName.includes('Persentase')) {
        return Utils.getPalette(chart.dataFields.values.length,
                                Utils.palette.backgroundColors[0])
      }
      else if(chart.chartName.includes('Jumlah')) {
        return Utils.getPalette(chart.dataFields.values.length,
                                Utils.palette.backgroundColors[2])
      }
    }
  }
  render() {
    return (
      <div className='ChartList row'>
        {this.props.chartList.map((chart, index) => 
          (<Graphic chartType={chart.chartType} 
                    chartName={chart.chartName}
                    dataFields={chart.dataFields}
                    dataOptions={chart.dataOptions}
                    key={index}
                    palette={this.getPalette(chart)}/>)
        )}
      </div>
    )
  }
}

ChartList.propTypes = {
  chartList: React.PropTypes.arrayOf(React.PropTypes.object)
}

module.exports = ChartList;