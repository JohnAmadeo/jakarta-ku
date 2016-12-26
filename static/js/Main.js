import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import JakartaMap from './JakartaMap';

class Main extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className='Main'>
        <JakartaMap />
      </div>
    )
  }
}

module.exports = Main;