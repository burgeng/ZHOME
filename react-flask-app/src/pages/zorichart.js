import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register required components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function ZORIChart({ data }) {
  // Extract dates and ZORI values from the data
  const labels = data.map((item) => item.date);
  const zoriValues = data.map((item) => item.zori);

  const chartData = {
    labels: labels, // x-axis labels
    datasets: [
      {
        label: 'Zillow Observed Rent Index (ZORI)',
        data: zoriValues, // y-axis data
        fill: false,
        borderColor: 'darkblue',
        tension: 0.3, // smooth curve
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Date',
        },
      },
      y: {
        title: {
          display: true,
          text: 'ZORI',
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
}

export default ZORIChart;
