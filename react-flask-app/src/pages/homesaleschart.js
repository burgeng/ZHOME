import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

// Register required components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function HomeSalesChart({ data }) {
  // Extract dates and MHI values from the data
  const labels = data.map((item) => item.date);
  const mhi = data.map((item) => item.count);

  const chartData = {
    labels: labels, // x-axis labels
    datasets: [
      {
        label: 'Total Home Sales Count',
        data: mhi, // y-axis data
        backgroundColor: 'rgba(0, 0, 139, 0.7)', // semi-transparent dark blue
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
          text: 'Count',
        },
      },
    },
  };

  return <Bar data={chartData} options={options} />;
}

export default HomeSalesChart;
