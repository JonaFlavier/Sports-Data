import React from "react";
import CanvasJSReact from "@canvasjs/react-charts";

var CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

function Histogram({ title, data }) {
  //   console.log("histogram here");
  //   console.log(data);

  const options = {
    animationEnabled: true,
    exportEnabled: true,
    theme: "dark1",
    axisY: {
      // prefix: "",
      //gridThickness: 0,
      tickLength: 0,
      title: "Win Percentage of Matches",
      includeZero: true,
    },
    axisX: {
      title: "Simulation Results",
    },
    legend: {
      cursor: "pointer",
      itemclick: function (e) {
        if (
          typeof e.dataSeries.visible === "undefined" ||
          e.dataSeries.visible
        ) {
          e.dataSeries.visible = false;
        } else {
          e.dataSeries.visible = true;
        }
        e.chart.render();
      },
    },
    toolTip: {
      shared: true,
    },
    data: [
      {
        type: "column",
        name: data.home_team.name,
        showInLegend: true,
        color: "#585f64",
        dataPoints: data.bins.map((item, index) => {
          return { label: item, y: data.sim_data[0][index] };
        }),
      },
      {
        type: "column",
        name: data.away_team.name,
        color: "#c43138",
        showInLegend: true,
        dataPoints: data.bins.map((item, index) => {
          return { label: item, y: data.sim_data[1][index] };
        }),
      },
    ],
  };
  return (
    <div style={{ width: "100%", margin: "20px" }}>
      <p>{data.date}</p>
      <CanvasJSChart options={options} />
    </div>
  );
}

export default Histogram;
