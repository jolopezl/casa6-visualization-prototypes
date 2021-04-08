import logo from './logo.svg';
import './App.css';
import Plotly from 'plotly.js'
import createPlotlyComponent from 'react-plotly.js/factory'

const Plot  = createPlotlyComponent(Plotly);

function App() {

  const data = {
    data: [{
      x: [10.0,
        8.66158094405463,
        5.004596890082058,
        0.007963267107334854,
        -4.9908019935561985,
        -8.653610355694578,
        -9.999987317275394,
        -8.669529561925529,
        -5.018379092223095,
        -0.023889781122815385,
        4.976994437636892,
        8.645617817063133],
      y: [0.0,
          4.997701026431024,
          8.657598394923443,
          9.999996829318347,
          8.665558000562658,
          5.011489580136383,
          0.01592652916486828,
          -4.983899795832512,
          -8.649616828896994,
          -9.99997146387718,
          -8.673495625624737,
          -5.0252654219733],
      type: 'scatter',
      mode: 'markers',
      marker: {
        color: '#0000ff',
        opacity: 0.5,
        size: 12, 
        line: {
          color: '#00000f',
          width: 2}
      },
      name: 'points'
    }],
    layout: {
        plotBackground: '#00000f',
        autosize: false, 
        width: 450,
        height: 450,
        margin: {t:20, r: 20, l: 20, b: 20},
        yaxis: {
          title: {
            text: "y pos (km)"
          }
        },
        xaxis: {
          title: {
            text: "x pos (km)"
          }
        }
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <p> CASA plotants demo using Electron and React.js </p>
        <div>
          <p align='left'>Measurement set: <input id="input-dataset" value="Type the MS path here..."></input></p>
          <p align='left'>Options: <input id="input-plot-options" value="Plot options here..."></input></p>
          <Plot data={data.data} layout={data.layout} config={{displayModeBar: false}} />
        </div>
        <div id="dummy-div">
          
        </div>
      </header>
    </div>
  );
}

export default App;
