import React from 'react';
import ReactDOM from 'react-dom';
import ClassNames from 'classnames';

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
  const cssClasses = ClassNames({
    'btn': true, 
    'btn-lg': true, 
    'btn-default': true,
    'Button': true,
    'is-selected': props.isSelected
  });

  return (
      <button 
        type="button"
        className={cssClasses}       
        onClick={props.onButtonClick} key={props.key}>
        {props.isSelected ? (<span>&minus; &nbsp;</span>) : 
                          (<span>&#43; &nbsp;</span>)} 
        {props.text}
      </button>
  )
}

module.exports = Button;