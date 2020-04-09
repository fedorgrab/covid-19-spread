let currentDayOne;

const GREEN = "#9aff78";
const GREEN_WHITE = "#23880f";
const BACKGROUND = "#192331";
const BACKGROUND_WHITE = "#ededed";
const RED = "#f6766c";
const RED_WHITE = "#b61b13";
const WHITE = "#FFFFFF";
const BLACK = "#1d1d1d";
const GRAY_SMALL = "#DFDFDF";
const GRAY_SMALL_WHITE = "#575757";


function plot(dayOneData, styleType) {
  let div = document.getElementById("country-timeline-stat");
  let country = dayOneData[0].node.country;
  var xData = [
    dayOneData.map(function (el) {
      return el.node.date
    }),
    dayOneData.map(function (el) {
      return el.node.date
    }),
    dayOneData.map(function (el) {
      return el.node.date
    }),
  ];
  
  var yData = [
    dayOneData.map(function (el) {
      return el.node.casesConfirmed
    }),
    dayOneData.map(function (el) {
      return el.node.casesDeaths
    }),
    dayOneData.map(function (el) {
      return el.node.casesRecovered
    }),
  ];
  let numberOfPoints = yData[0].length;
  let colors = styleType === "white" ? [BLACK, RED_WHITE, GREEN_WHITE] : [WHITE, RED, GREEN];
  let background = styleType === "white" ? BACKGROUND_WHITE : BACKGROUND;
  let xtickColor = styleType === "white" ? GRAY_SMALL_WHITE : GRAY_SMALL;
  var lineSize = [4, 2, 2];
  let labels = ['Confirmed', 'Deaths', 'Recovered'];
  var data = [];
  
  
  for (var i = 0; i < xData.length; i++) {
    var result = {
      x: xData[i].slice(0, numberOfPoints),
      y: yData[i].slice(0, numberOfPoints),
      type: 'scatter',
      mode: 'lines',
      name: labels[i],
      line: {
        color: colors[i],
        width: lineSize[i]
      }
    };
    var result2 = {
      x: [xData[i][numberOfPoints - 1]],
      y: [yData[i][numberOfPoints - 1]],
      type: 'scatter',
      mode: 'markers',
      hoverinfo: 'none',
      name: labels[i],
      marker: {color: colors[i], size: 12}
    };
    data.push(result, result2);
  }
  let width = isMobile ?  $(window).width(): 300;
  let height = isMobile ? 200: 300;
  
  var layout = {
    showlegend: false,
    height: height,
    width: width,
    plot_bgcolor: background,
    paper_bgcolor: background,
    dtick: 3,
    
    xaxis: {
      showline: true,
      showgrid: false,
      showticklabels: true,
      fixedrange: true,
      linecolor: xtickColor,
      linewidth: 2,
      tickwidth: 2,
      ticklen: 5,
      tickfont: {family: 'Roboto', size: 10, color: xtickColor}
    },
    yaxis: {
      showgrid: false,
      zeroline: false,
      fixedrange: true,
      showline: false,
      showticklabels: false
    },
    autosize: false,
    margin: {
      autoexpand: false,
      l: 15,
      r: 15,
      t: 40,
      b: 50
    },
    annotations: [
      {
        xref: 'paper',
        yref: 'paper',
        x: 0.0,
        y: 1.05,
        xanchor: 'left',
        yanchor: 'bottom',
        text: `${country} Timeline`,
        font: {
          family: 'Roboto',
          size: 14,
          color: xtickColor
        },
        showarrow: false
      },
    ]
  };
  Plotly.newPlot(div, data, layout, {displayModeBar: false});
}

function restylePlot(styleType) {
  plot(currentDayOne, styleType);
}
