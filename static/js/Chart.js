import React from 'react';
import ReactDOM from 'react-dom'
import Utils from './utils';
import Chart from './Chart';
import {HorizontalBar, Bar, Doughnut} from 'react-chartjs-2';

{/* Props
  - selectedCategory (string)
    name of currently selected category

  - selectedComparison (string)
    name of currently selected comparison

  - selectedRegionList (array of strings)
    array of names of all currently selected regions

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
    return null;
  }
}

module.exports = Chart;