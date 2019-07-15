import React from 'react';
import './App.css';
import axios from 'axios';

const axiosInstance = axios.create({ baseURL: 'http://127.0.0.1:5000/', timeout: 30000 });

class StackInputComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: '', resolvedStack: null };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    const self = this;

    axiosInstance.post('/symbolizestack', {
      stack: self.state.value,
    }).then(function (response) {
      self.setState({ resolvedStack: response.data.buildInfo });
    }).catch(function (error) {
      self.setState({ resolvedStack: error });
    });

    event.preventDefault();
  }

  render() {
    const state = this.state;

    return (
      <div className="stackInput">
        <form onSubmit={this.handleSubmit}>
          <div>
            <label>
              Name:
            </label>
            <div>
              <textarea rows={50} cols={60} value={state.value} onChange={this.handleChange} />
            </div>
            <div>
              <input type="submit" value="Submit" />
            </div>
          </div>
        </form>
        {state.resolvedStack ? (
          <div>
            <label>
              Resolved stack:
          </label>
            <div>
              <textarea rows={50} cols={60} value={state.resolvedStack} />
            </div>
          </div>
        ) : (<div />)}
      </div>
    );
  }
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          <StackInputComponent id="stack" />
        </p>
      </header>
    </div>
  );
}

export default App;
