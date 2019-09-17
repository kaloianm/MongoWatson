import React from 'react';
import './App.css';
import axios from 'axios';

const axiosInstance = axios.create({ baseURL: 'http://127.0.0.1:5000/', timeout: 30000 });

class StackFrames extends React.Component {
  render() {
    const stackFrames = this.props.stackFrames;

    return (
      <div>
        {stackFrames.map(function (frame) {
          return (<p><a href={frame.url}>{frame.fn}</a></p>);
        })}
      </div>);
  }
}

class StackInputComponent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      stack: null,
      resolvedStack: null
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ stack: event.target.value });
  }

  handleSubmit(event) {
    const self = this;
    const state = this.state;

    axiosInstance.post('/symbolizestack', {
      stack: state.stack,
    }).then(function (response) {
      self.setState({ resolvedStack: response.data });
    }).catch(function (error) {
      self.setState({ resolvedStack: error });
    });

    event.preventDefault();
  }

  render() {
    const self = this;
    const state = this.state;

    return (
      <div>
        <form onSubmit={self.handleSubmit}>
          <div>
            <label>
              Stack:
            </label>
            <div>
              <textarea rows={28} cols={100} value={state.value} onChange={self.handleChange} />
            </div>
            <div>
              <input type="submit" value="Submit" />
            </div>
          </div>
        </form>

        {state.resolvedStack ? (
          <div>
            <label>
              Resolved stack for build version: {state.resolvedStack.buildInfo.version}
            </label>
            <StackFrames stackFrames={state.resolvedStack.stackFrames} />
          </div>
        ) : (<div />)}
      </div>
    );
  }
}

function App() {
  return (
    <div className="App">
      <script type="text/javascript" src="https://gist-it.appspot.com/assets/prettify/prettify.js"></script>
      <link rel="stylesheet" href="https://gist-it.appspot.com/assets/embed.css" />
      <link rel="stylesheet" href="https://gist-it.appspot.com/assets/prettify/prettify.css" />

      <header className="App-header">
        <p>
          <StackInputComponent id="stack" />
        </p>
      </header>
    </div>
  );
}

export default App;
