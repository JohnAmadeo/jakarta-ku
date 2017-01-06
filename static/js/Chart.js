import React from 'react';
import ReactDOM from 'react-dom'
import Utils from './utils';
import {HorizontalBar, Bar, Doughnut} from 'react-chartjs-2';

{/* Props
  - chartData (object)
    {
      label_list: ['SD', 'SMP', 'SMA'],
      dat_list: [50, 34, 67]
    }
  - chartOptions (object)
    {
      field_axis_label: 'Jumlah Orang', // if bar chart
      measure_axis_label: ' Tingkat Pendidikan', // if bar chart
      tooltip_format: ['NUMBER', 'orang'] // run reduce on array later
                                          // and replace 'NUMBER' w/
                                          // actual value
    }

*/}
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
class Chart extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    var barData = {
        labels: ["Tidak Sekolah", "Belum Tamat/Selesai SD", "SMP", "SMA", "S1", "S2", "Tidak Sekolah", "Belum Tamat/Selesai SD", "SMP", "SMA", "S1", "S2"],
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
                data: [65, 59, 80, 81, 56, 35, 65, 59, 80, 81, 56, 35]
            }
        ]
    };
    var barOptions = {
      maintainAspectRatio: false,
      responsive: true,
      legend: {
        display: false
      },
      scales: {
        yAxes: [{
          ticks: {
            min: 0,
            mirror: true
          },
          scaleLabel: {
            display: true,
            labelString: 'Jumlah Orang'
          }
        }],
        xAxes: [{
          ticks: {
            callback: function(label) {
              if(label.length > 3) {
                return (label.substr(0,3)) + '...';
              }
              else return label
            },
            fontSize: 12
          },
          scaleLabel: {
            display: true,
            labelString: 'Tingkat Pendidikan'
          }
        }]
      },
      tooltips: {
        callbacks: {
          label: (item) => (item.xLabel + ' Orang')
        }
      }
    };
    var pieData = {
        labels: ["Tidak Sekolah", "Belum Tamat/Selesai SD", "SD", "SMP", "SMA", "D1", "D2", "D3", "S1", "S2"],
        datasets: [
            {
                data: [0.65, 0.59, 0.80, 0.81, 0.56, 0.35, 0.23, 0.45, 0.70, 0.55],
                backgroundColor: [
                  'rgba(255, 131, 131, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)',
                  'rgba(99, 234, 255, 0.2)',
                  'rgba(252, 110, 63, 0.2)',
                  'rgba(79, 247, 135, 0.2)',
                  'rgba(96, 120, 255, 0.2)',
                ],
                borderColor: [
                  'rgba(255,131,131,1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)',
                  'rgba(99, 234, 255, 1)',
                  'rgba(252, 110, 63, 1)',
                  'rgba(79, 247, 135, 1)',
                  'rgba(96, 120, 255, 1)',
                ],
                hoverBackgroundColor: [
                  'rgba(255,131,131,1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)',
                  'rgba(99, 234, 255, 1)',
                  'rgba(252, 110, 63, 1)',
                  'rgba(79, 247, 135, 1)',
                  'rgba(96, 120, 255, 1)',
                ]
            }]
    };
    var pieOptions = {
      maintainAspectRatio: true,
      legend: {
        display: true
      }
    }
    console.log(document.getElementsByClassName('Chart'));
    return (
      <div className='ChartList row'>
        <div className='col-lg-6'>
          <div className='Chart'>
            <h3 style={{
              'color': '#FF8383'
            }}> 
              Jumlah Orang per Tingkat Pendidikan
            </h3>
            {/*<HorizontalBar data={barData} options={barOptions}/>*/}
            <Doughnut data={pieData} options={pieOptions} width={520} height={420}/>
          </div>
        </div>
      </div>
    )
  }
}

module.exports = Chart;