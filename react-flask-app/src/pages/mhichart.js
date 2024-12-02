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

function MHIChart({ data }) {
  // Extract dates and ZHVI values from the data
  const labels = data.map((item) => item.date);
  const mhi = data.map((item) => item.mhi);

  const chartData = {
    labels: labels, // x-axis labels
    datasets: [
      {
        label: 'Market Heat Index (MHI)',
        data: mhi, // y-axis data
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
          text: 'MHI',
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
}

export default MHIChart;
