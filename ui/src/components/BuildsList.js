import React from 'react';

class BuildsListState {
  constructor() {
    this.os = null;
    this.availableBuilds = [{ disabled: true, selected: true, label: '-- Select OS --' }];
    this.selectedBuild = null;

    this.listeners = [];
  }

  setOS(newOS) {
    this.os = newOS;
    this.availableBuilds = [{ disabled: true, selected: true, label: 'Loading ...' }];
    this.notifyStateChanged();
  }

  setAvailableBuilds(builds) {
    this.availableBuilds = builds;
    this.notifyStateChanged();
  }

  registerListener(fn) {
    this.listeners.push(fn);
  }

  notifyStateChanged() {
    for (let listener of this.listeners) {
      listener();
    }
  }
}

/**
 * Fetches and renders a list of the available
 */
export default class BuildsList extends React.Component {
  constructor(props) {
    super(props);

    const self = this;

    this.axios = props.environment.axios;

    props.state.registerListener(function () {
      self.setState({ state: 0 });
    });

    this.onOSChange = this.onOSChange.bind(this);
    this.onBuildChange = this.onBuildChange.bind(this);
  }

  onOSChange(event) {
    const state = this.props.state;
    state.setOS(event.target.value);

    this.axios.get('/listbuilds', {
      params: { buildOS: state.os }
    }).then(function (response) {
      state.setAvailableBuilds(response.data.split('\n')
        .map(function (el) {
          try {
            return JSON.parse(el);
          } catch (err) {
            return { disabled: true, label: err.toString() };
          }
        })
        .map(function (el) { return { disabled: false, label: el.name, url: el.url }; }));
    }).catch(function (error) {
      state.setAvailableBuilds([{ disabled: false, selected: true, label: error.toString() }]);
    });
  }

  onBuildChange(event) {
    this.props.state.selectedBuild = event.target.value;
  }

  render() {
    const self = this;
    const state = self.props.state;

    return (
      <div>
        <label>Operating system:</label>
        <div>
          <select value={state.os} onChange={self.onOSChange}>
            <option disabled={true} selected={true}> -- Select OS -- </option>
            <option value="osx">macOS 64-bit x64</option>
            <option value="linux/x86_64-ubuntu1604">Ubuntu 16.04 Linux 64-bit x64</option>
          </select>
        </div>

        <label>Build:</label>
        <div>
          <select value={state.selectedBuild} onChange={self.onBuildChange}>
            {
              state.availableBuilds.map(
                (el) => <option disabled={el.disabled} selected={el.selected} value={el.url}>{el.label}</option>)
            }
          </select>
        </div>
      </div>
    );
  }
}
