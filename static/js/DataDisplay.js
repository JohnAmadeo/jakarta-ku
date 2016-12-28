import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import JakartaMap from './JakartaMap';
import Button from './Button';

{/* Props
  - selectedCategory (string)
    name of currently selected category
*/}
class DataDisplay extends React.Component {
  constructor(props) {
    super(props);
    this.onSelectComparison = this.onSelectComparison.bind(this);

    this.state = {
      selectedComparison: "category"
    }
  }
  onSelectComparison(comparison, event) {
    this.setState({
      selectedComparison: comparison
    })
  }
  render() {
    return (
      <div className="DataDisplay">
        <div className="container">
          <ComparisonBar 
            onSelectComparison={this.onSelectComparison}
            selectedComparison={this.state.selectedComparison} />
          <LoremIpsum />
        </div>
      </div>
    )
  }
}

DataDisplay.propTypes = {
  selectedComparison: React.PropTypes.oneOf(["category", "region"])
}

{/* Props
  - onSelectComparison (function)
    event handler function that updates the state of the 
    currently selected comparison

  - selectedComparison (string)
    name of currently selected comparison
*/}
class ComparisonBar extends React.Component {
  constructor(props) {
    super(props);
    this.isComparisonSelected = this.isComparisonSelected.bind(this);
  }
  isComparisonSelected(comparison) {
    return this.props.selectedComparison === comparison;
  }
  render() {
    return (
      <div className="ComparisonBar">
        <Button 
          key={1} text={"Bandingkan kategori"} 
          selected={this.isComparisonSelected("category")}
          onButtonClick={this.props.onSelectComparison
                                   .bind(this, "category")}/>
        <Button 
          key={2} text={"Bandingkan kecamatan"}
          selected={this.isComparisonSelected("region")}
          onButtonClick={this.props.onSelectComparison
                                   .bind(this, "region")}/>
      </div>
    )
  }
}

const LoremIpsum = (props) => {
  return (
    <p>
      "It is a period of civil war. Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire.
      During the battle, Rebel spies managed to steal secret plans to the Empire's ultimate weapon, the DEATH STAR, an armored space station with enough power to destroy an entire planet.
      Pursued by the Empire's sinister agents, Princess Leia races home aboard her starship, custodian of the stolen plans that can save her people and restore freedom to the galaxy....
    </p>
  )
}

module.exports = DataDisplay;
  