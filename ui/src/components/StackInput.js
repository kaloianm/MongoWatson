import React from 'react';

import StackFrames from './StackFrames';

export default class StackInput extends React.Component {
  constructor(props) {
    super(props);

    this.axios = props.environment.axios;

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

    self.setState({ loading: true });

    self.axios.post('/symbolizestack', {
      stack: state.stack,
    }).then(function (response) {
      self.setState({ loading: undefined, result: response.data });
    }).catch(function (error) {
      self.setState({ loading: undefined, error: error });
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

        <div>
          {(() => {
            if (state.loading) {
              return (
                <div>
                  <h2>Loading stack ...</h2>
                </div>
              );
            } else if (state.result) {
              return (
                <div>
                  <h1>Resolved stack for {state.result.buildInfo.uname.sysname} {state.result.buildInfo.edition} build version {state.result.buildInfo.version}</h1>
                  <h2>Seen {state.result.occurrences} times so far</h2>
                  <StackFrames stackFrames={state.result.stackFrames} />
                </div>);
            } else if (state.error) {
              return (
                <div>
                  Failed to process the stack due to error:
                  <p>
                    {JSON.stringify(state.error)}
                  </p>
                </div>);
            }
          })()}
        </div>
      </div>
    );
  }
}
