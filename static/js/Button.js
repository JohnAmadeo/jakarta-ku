import React from 'react';
import ReactDOM from 'react-dom';
import ClassNames from 'classnames';

{/* Props
  - onButtonClick (function)
    event handler function executed when button is clicked    
  - isSelected (boolean)
    true if button is selected; false otherwise
  - onHover (function)
    event handler function executed when button is hovered over
  - isHoveredOver (boolean)
    true if button is hovered over; false otherwise
  - text (string)
    text the button should display
*/}

const Button = (props) => {
  const cssClasses = ClassNames({
    'btn': true, 
    'btn-lg': true, 
    'btn-default': true,
    'Button': true,
    'is-selected': props.isSelected,
    'is-hovered-over': props.isHoveredOver
  });

  return (
      <button type="button" key={props.key}
              className={cssClasses}       
              onClick={props.onButtonClick}
              onMouseOver={props.onHover}
              onMouseOut={props.onHover}>

        {(props.isSelected || props.isHoveredOver) ? 
          (<span>&minus; &nbsp;</span>) : (<span>&#43; &nbsp;</span>)} 
        {props.text}

      </button>
  )
}

module.exports = Button;