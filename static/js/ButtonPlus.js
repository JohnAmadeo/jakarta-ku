import React from 'react';
import ReactDOM from 'react-dom'

class ButtonPlus extends React.Component {
  constructor(props) {
    super(props);
    this.getSymbol = this.getSymbol.bind(this);
  }
  getSymbol(isSelected) {
    return isSelected ? (<span>&minus; &nbsp;</span>) :
                        (<span>&#43; &nbsp;</span>)
  }
  render() {
    return (
      <button type="button" className="btn btn-lg btn-default"
              onClick={this.props.onButtonClick} key={this.props.key}>
        {this.getSymbol(this.props.isSelected)} 
        {this.props.text}
      </button>
    )
  }
}

module.exports = ButtonPlus
