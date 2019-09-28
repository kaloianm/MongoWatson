import React from 'react';

/**
 * Renders a table with the stack frames specified in the 'stackFrames' property.
 */
export default class StackFrames extends React.Component {
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

  scrollToMyRef = () => this.resolvedStackRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
