import React, { Component } from "react";

class Search extends Component {
  state = {
    query: "",
  };

  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch(this.state.query);
  };

  handleInputChange = () => {
    this.setState({
      query: this.search.value,
    });
  };

  render() {
    return (
      <form onSubmit={this.getInfo}>
        <input
          className="p-2"
          placeholder="Search questions..."
          ref={(input) => (this.search = input)}
          onChange={this.handleInputChange}
        />
        <input
          type="submit"
          value="Submit"
          className="bg-blue-500 inline-block p-2 text-white mt-3"
        />
      </form>
    );
  }
}

export default Search;
