import React from 'react';
import ReactDOM from 'react-dom'
import UUID from 'uuid/v4';
import Store from 'store2';

class Main extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className='Main'>
        <Sample />
      </div>
    )
  }
}

const Sample = (props) => {
  return (
    <div className='Sample'>
    </div>
  )
}

module.exports = Main;