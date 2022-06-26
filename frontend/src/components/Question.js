import React, { Component } from "react";
import "../stylesheets/Question.css";

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }
  render() {
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className="Question-holder">
        <div className="Question">{question}</div>
        <div className="Question-status">
          <img
            className="category"
            alt={`${category.toLowerCase()}`}
            src={`${category.toLowerCase()}.svg`}
          />
          <div className="difficulty">Difficulty: {difficulty}</div>
          <img
            src="delete.png"
            alt="delete"
            className="delete"
            onClick={() => this.props.questionAction("DELETE")}
          />
        </div>
        <div
          className="bg-blue-500 w-auto inline-block px-5 py-2 text-white rounded shadow-lg mt-4 cursor-pointer hover:shadow-xl hover:bg-blue-600"
          onClick={() => this.flipVisibility()}
        >
          {this.state.visibleAnswer ? "Hide" : "Show"} Answer
        </div>
        <div className="answer-holder">
          <span
            style={{
              visibility: this.state.visibleAnswer ? "visible" : "hidden",
            }}
          >
            Answer: {answer}
          </span>
        </div>
      </div>
    );
  }
}

export default Question;
