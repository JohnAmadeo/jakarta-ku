import React from 'react';
import ReactDOM from 'react-dom'

{/* Props
  - onButtonClick (function)
    event handler function executed when button
    is clicked    
  - selected (boolean)
    true if button is selected; false otherwise
  - text (string)
    text the button should display
*/}

const Button = (props) => {
  return (
    <button type="button" className="btn btn-lg btn-default"
            onClick={props.onButtonClick} key={props.key}>
      {props.selected ? (<span>&minus; &nbsp;</span>) : 
                        (<span>&#43; &nbsp;</span>)} 
      {props.text}
    </button>
  )
}

module.exports = Button;