import React from 'react';
import './App.css';
import axios from 'axios';

const axiosInstance = axios.create({ baseURL: 'http://127.0.0.1:5000/', timeout: 30000 });

/**
 * Renders a table with the stack frames specified in the 'stackFrames' property.
 */
class StackFrames extends React.Component {
  constructor(props) {
    super(props);

    this.resolvedStackRef = React.createRef();
  }

  render() {
    const stackFrames = this.props.stackFrames;
    var stackFrameNumber = 0;

    return (
      <div align='left' ref={this.resolvedStackRef}>
        <table>
          {stackFrames.map(function (frame) {
            return (
              <tr>
                <td align='right'>
                  {(stackFrameNumber++) + ':'}
                </td>
                <td nowrap>
                  <a href={frame.url} target='_blank' rel='noopener noreferrer'>{frame.fn}</a>
                </td>
              </tr>
            );
          })}
        </table>
      </div>);
  }

  scrollToMyRef = () => window.scrollTo(0, this.resolvedStackRef.current.offsetTop)
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
            <h1>Resolved stack for {state.resolvedStack.buildInfo.uname.sysname} {state.resolvedStack.buildInfo.edition} build version {state.resolvedStack.buildInfo.version}</h1>
            <h2>Seen {state.resolvedStack.occurrences} times so far</h2>
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
        <div>
          <img src="doctor.png" alt="doctor" width="100px" />
        </div>
        <div>
          <label>
            Stack:
        </label>
          <p>
            <StackInputComponent id="stack" />
          </p>
        </div>
      </header>
    </div>
  );
}

export default App;
