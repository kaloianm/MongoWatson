import React from 'react';

import StackInput from './components/StackInput'

import './App.css';

function App(props) {
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
            <StackInput id="stack" environment={props.environment} />
          </p>
        </div>
      </header>
    </div>
  );
}

export default App;
