import React from 'react';
import ReactDOM from 'react-dom'
import Utils from './utils';

import {HorizontalBar, Bar, Doughnut} from 'react-chartjs-2';
import Measure from 'react-measure';

{/*
  Abstraction Specifications
  - Two chart types: 'AdaptiveBar' and 'AdaptiveDoughnut'
  - AdaptiveBar Specifications
      - Below col-lg breakpoint:
          - Horizontal Bar w/ mirrored ticks
          - Size takes up entire screen
      - Above col-lg breakpoint:
          - Vertical Bar
          - Truncated labels w/ ellipsis ending
            - Make sure tooltip strings are not truncated
          - More than x bars:
            - Make size col-lg-12
          - Less than x bars:
            - Make size col-lg-6
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
                  width={this.state.width}/>
      )
    }
    else if(this.props.chartType === 'doughnut') {
      return (
        <DoughnutChart dataFields={this.props.dataFields} 
                       dataOptions={this.props.dataOptions} 
                       width={this.state.width}/>
      )
    }
  }
  onUpdateDimensions(dimensions) {
    this.setState({
      width: dimensions.width,
      height: dimensions.height
    })
  }
  render () {

    return (
      <Measure onMeasure={this.onUpdateDimensions}>
        <div className='Graphic'>
          <Label text={this.props.chartName} />
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
*/}

class BarChart extends React.Component {
  constructor(props) {
    super(props);
    this.getChartData = this.getChartData.bind(this);
    this.getChartOptions = this.getChartOptions.bind(this);
    this.getTooltipTitle = this.getTooltipTitle.bind(this);
    this.getTooltipLabel = this.getTooltipLabel.bind(this);
    this.getTickLabel = this.getTickLabel.bind(this);
    this.getDimensions = this.getDimensions.bind(this);

    this.maxBarWidth = 130;
    this.maxBarHeight = 450;
    this.horizontalBarWidth = 50;
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
    const widthPct = numBars * this.maxBarWidth / windowWidth * 100;
    const fontSize = 12;
    let lengthLimit = 0;

    if(widthPct < 100) {
      lengthLimit = Math.round(this.maxBarWidth / fontSize) + 2; 
      console.log(lengthLimit);    
    }
    else {      
      lengthLimit = Math.round(
                      (100/widthPct) * 
                      (Math.round(this.maxBarWidth / fontSize) + 2)
                    ); 
      // console.log(lengthLimit);
    }

    console.log(widthPct);

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
  getDimensions() {
    const windowWidth = $(window).width();
    const numBars = this.props.dataFields.values.length;
    let divStyle = {};
    if(windowWidth < 1200) {
      const height = this.horizontalBarWidth * numBars;
      divStyle.height = height + 'px';
      divStyle.width = '95%';
    }
    else {
      divStyle.height = this.maxBarHeight + 'px';
      const width = numBars * this.maxBarWidth / windowWidth * 100;
      divStyle.width = width > 100 ? '100%' : (width + '%');
      console.log(width);
    }

    return divStyle;
  }
  render() {
    let windowWidth = $(window).width();
    return (
      <div className='BarChart' style={this.getDimensions()}>
        {windowWidth < 1200 ? 
        <HorizontalBar data={this.getChartData()} 
                       options={this.getChartOptions()} />     
        :
        <Bar data={this.getChartData()} 
             options={this.getChartOptions()} />
        }                                            
        <p>{windowWidth}</p>
      </div>
    )
  }
}

class DoughnutChart extends React.Component {
  constructor(props) {
    super(props);
    this.getChartData = this.getChartData.bind(this);
    this.getChartOptions = this.getChartOptions.bind(this);
    this.getChartSize = this.getChartSize.bind(this)
  }
  getChartData() {

  }
  getChartOptions() {

  }
  getChartSize() {

  }
  render() {
    return (
      <Doughnut data={this.getChartData()} options={this.getChartOptions()} width={this.getChartSize()}/>
    )
  }
}

const Label = (props) => {
 return(
   <p className="Label">
     {props.text}
   </p>
 )
}

module.exports = Graphic;