import React from 'react';
import ReactDOM from 'react-dom'
import Utils from './utils';

import {HorizontalBar, Bar, Doughnut} from 'react-chartjs-2';
import Measure from 'react-measure';

{/*
  Abstraction Specifications
  - AdaptiveDoughnut Specifications
      - Modify chart width/height ratio at multiple breakpoints to
        prevent chart from being too big
      - Above col-lg breakpoint, make size col-lg-6
  - Color Specifications
    - Strong border colors, and faded inner colors
    - Inner color becomes border colors on hover
*/}

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
      fieldAxis: 'Pekerjaan'
      measureAxis: 'Jumlah Orang'
      tooltipStringFormat: //func?
    }
*/}

class Graphic extends React.Component {
  constructor(props) {
    super(props);
    this.renderChart = this.renderChart.bind(this);
    this.onUpdateDimensions = this.onUpdateDimensions.bind(this);
    this.getDimensions = this.getDimensions.bind(this);

    this.maxBarWidth = 130;
    this.maxBarHeight = 450;
    this.horizontalBarWidth = 50;

    this.state = {
      width: 0,
      height: 0
    }
  }
  renderChart() {
    if(this.props.chartType === 'bar') {
      return (
        <BarChart dataFields={this.props.dataFields}
                  dataOptions={this.props.dataOptions} 
                  maxBarWidth={this.maxBarWidth}/>
      )
    }
    else if(this.props.chartType === 'doughnut') {
      return (
        <DoughnutChart dataFields={this.props.dataFields} 
                       dataOptions={this.props.dataOptions}/>
      )
    }
  }
  onUpdateDimensions(dimensions) {
    this.setState({
      width: dimensions.width,
      height: dimensions.height
    })
  }
  getDimensions() {
    let divStyle = {};
    const windowWidth = $(window).width();
    const numValues = this.props.dataFields.values.length;

    if(this.props.chartType === 'bar') {
      if(windowWidth < 1200) {
        const height = (this.horizontalBarWidth * numValues) + 91;
        divStyle.height = height + 'px';
        divStyle.width = '95%';
      }
      else {
        divStyle.height = this.maxBarHeight + 'px';
        const widthPct = (numValues * this.maxBarWidth + 127) / 
                         windowWidth * 100;
        divStyle.width = widthPct > 100 ? '100%' : (widthPct + '%');
        console.log(widthPct);
      }
    }
    else if(this.props.chartType === 'doughnut') {
      let componentWidth = 0;
      if(windowWidth < 1200) {
        componentWidth = 0.85 * 0.95 * windowWidth;
        divStyle.width = '95%';
      }
      else {
        componentWidth = 0.85 * 0.40 * windowWidth;   
        divStyle.width = '40%';    
      }

      const avgLabelLength = 
        this.props.dataFields.labels
        .reduce((sum, label) => sum + label.length, 0)
        * 12 / numValues;

      const numLegendLines = 
        Math.round((numValues * (avgLabelLength + 50)) / componentWidth);
      const height = 300 + (numLegendLines * 20);

      divStyle.height =  height + 'px'; 
    }
    return divStyle;
  }
  render () {

    return (
      <Measure onMeasure={this.onUpdateDimensions}>
        <div className='Graphic' style={this.getDimensions()}>
          <Title text={this.props.chartName} />
          {/*<SharingBar />*/}
          {this.renderChart()}
        </div>
      </Measure>
    )
  }
}

{/* Props 
    dataFields (object)
    {
      values: [1,2,3],
      labels: ['a','b','c']
    }

    dataOptions (object)
    {
      fieldAxis: 'Pekerjaan'
      measureAxis: 'Jumlah Orang'
      tooltipStringFormat: //func?
    }

    maxBarWidth (integer)
    - maximum width of a bar in a chart
*/}

class BarChart extends React.Component {
  constructor(props) {
    super(props);
    this.getChartData = this.getChartData.bind(this);
    this.getChartOptions = this.getChartOptions.bind(this);
    this.getTooltipTitle = this.getTooltipTitle.bind(this);
    this.getTooltipLabel = this.getTooltipLabel.bind(this);
    this.getTickLabel = this.getTickLabel.bind(this);
  }
  getChartData() {
    const palette = Utils.getColorPalette(this.props.dataFields.labels.length);
    const barData = {
        labels: this.props.dataFields.labels,
        datasets: [
            {
                backgroundColor: palette.background,
                borderColor: palette.border,
                borderWidth: 1,
                data: this.props.dataFields.values
            }
        ]
    };
    return barData;
  }
  getChartOptions() {
    const isBar = $(window).width() < 1200 ? false : true;
    const tooltipStringFormat = this.props.dataOptions.tooltipStringFormat;
    const barOptions = {
      maintainAspectRatio: false,
      responsive: true,
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          ticks: {
            min: 0,
            callback: ((label) => label),
            mirror: isBar ? false : true,
            fontSize: 12
          },
          scaleLabel: {
            display: true,
            labelString: isBar ? this.props.dataOptions.measureAxis :
                                 this.props.dataOptions.fieldAxis
          }
        }],
        xAxes: [{
          ticks: {
            min: 0,
            callback: isBar ? this.getTickLabel : ((label) => label),
            fontSize: 12
          },
          scaleLabel: {
            display: true,
            labelString: isBar ? this.props.dataOptions.fieldAxis : 
                                 this.props.dataOptions.measureAxis
          }
        }]
      },
      tooltips: {
        callbacks: {
          label: this.getTooltipLabel,
          title: this.getTooltipTitle
        }
      }
    };
    return barOptions;
  }
  getTickLabel(label) {
    const windowWidth = $(window).width()
    const numBars = this.props.dataFields.values.length;
    const widthPct = numBars * this.props.maxBarWidth / windowWidth * 100;
    const fontSize = 12;
    let lengthLimit = 0;

    if(widthPct < 100) {
      lengthLimit = Math.round(this.props.maxBarWidth / fontSize) + 2; 
      console.log(lengthLimit);    
    }
    else {      
      lengthLimit = Math.round(
                      (100/widthPct) * 
                      (Math.round(this.props.maxBarWidth / fontSize) + 2)
                    ); 
    }

    if(label.length > lengthLimit) {
      return (label.substr(0,lengthLimit - 2)) + '..';
    }
    else return label;
  }
  getTooltipTitle(item) {
    return this.props.dataFields.labels[item[0].index];
  }
  getTooltipLabel(item) {
    const stringFormat = this.props.dataOptions.tooltipStringFormat;
    return stringFormat.reduce((sentence, phrase) => {
      if(phrase === '_') {
        return sentence + this.props.dataFields.values[item.index]
                        + ' ';
      }
      else return sentence + phrase + ' ';
    }, '')
  }
  render() {
    let windowWidth = $(window).width();
    return (
      <div className='BarChart' style={{width: '100%', height: '100%'}}>
        {windowWidth < 1200 ? 
        <HorizontalBar data={this.getChartData()} 
                       options={this.getChartOptions()} />     
        :
        <Bar data={this.getChartData()} 
             options={this.getChartOptions()} />
        }                                            
      </div>
    )
  }
}

class DoughnutChart extends React.Component {
  constructor(props) {
    super(props);
    this.getChartData = this.getChartData.bind(this);
    this.getChartOptions = this.getChartOptions.bind(this);
    this.getLegendLabel = this.getLegendLabel.bind(this);
  }
  getLegendLabel() {

  }
  getChartData() {
    const palette = Utils.getColorPalette(this.props.dataFields.labels.length);
    var pieData = {
        labels: this.props.dataFields.labels,
        datasets: [
          {
            backgroundColor: palette.background,
            borderColor: palette.border,
            hoverBackgroundColor: palette.border,
            data: this.props.dataFields.values
          }
        ]
    };
    return pieData;
  }
  getChartOptions() {
    var pieOptions = {
      maintainAspectRatio: false,
      legend: {
        display: true
      }
    };
    return pieOptions;
  }
  render() {
    return (
      <div className='DoughnutChart' 
           style={{width: '100%', height: '100%'}}>
      <Doughnut data={this.getChartData()} 
                options={this.getChartOptions()} />
      </div>
    )
  }
}

const Title = (props) => {
 return(
   <p className="Title">
     {props.text}
   </p>
 )
}

module.exports = Graphic;