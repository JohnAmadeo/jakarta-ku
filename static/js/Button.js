import React from 'react';
import ReactDOM from 'react-dom'

{/* Props
  - onButtonClick (function)
    event handler function executed when button
    is clicked    
  - isSelected (boolean)
    true if button is selected; false otherwise
  - text (string)
    text the button should display
*/}

const Button = (props) => {
  let cssClasses = {
    selection: props.isSelected ? 'selected' : 'not-selected'
  }

  return (
    <span className='Button'>
      <button 
        type="button"       
        className={'btn btn-lg btn-default ' + cssClasses.selection}
        onClick={props.onButtonClick} key={props.key}>
        {props.isSelected ? (<span>&minus; &nbsp;</span>) : 
                          (<span>&#43; &nbsp;</span>)} 
        {props.text}
      </button>
    </span>
  )
}

module.exports = Button;