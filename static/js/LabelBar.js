import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import Request from 'superagent';
import Axios from 'axios';
import Utils from './utils';

import Button from './Button';

class LabelBar extends React.Component {
  constructor(props) {
    super(props);
    this.onHoverOnLabel = this.onHoverOnLabel.bind(this);
    this.isLabelHoveredOver = this.isLabelHoveredOver.bind(this);
    this.state = {
      hoveredLabel: ''
    }
  }
  isLabelSelected(label) {
    return this.props.selectedLabelList.includes(label) ? true : false;
  }
  isLabelHoveredOver(label) {
    return label === this.state.hoveredLabel ? true : false;
  }
  onHoverOnLabel(label, event) {
    if(event.type === 'mouseout') {
      this.setState({
        hoveredLabel: ''
      })
    }
    else if(event.type === 'mouseover') {
      this.setState({
        hoveredLabel: label
      })
    }
  }
  render() {
    console.log(this.props);
    return (
      <div className='LabelBar'>
        {this.props.labelList.map((label, index) =>
          (<Button type='button' key={index}
                   text={label} 
                   isSelected={this.isLabelSelected(label)}
                   isHoveredOver={this.isLabelHoveredOver(label)}
                   onButtonClick={this.props.onSelectLabel
                                            .bind(this, label)}
                   onHover={this.onHoverOnLabel.bind(this, label)} />)
        )}
      </div>
    )
  }
}

module.exports = LabelBar;