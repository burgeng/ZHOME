import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function ZHVFChart({ data }) {
  console.log(data)
  const { month, quarter, year } = data[0]; // Assuming the first object contains the relevant data

  // Chart.js data configuration
  const chartData = {
    labels: ['Month', 'Quarter', 'Year'], // X-axis labels
    datasets: [
      {
        label: 'Growth (%)',
        data: [parseFloat(month), parseFloat(quarter), parseFloat(year)], // Y-axis values
        backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(54, 162, 235, 0.6)', 'rgba(255, 99, 132, 0.6)'], // Bar colors
        borderColor: ['rgba(75, 192, 192, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)'],
        borderWidth: 1,
      },
    ],
  };

  // Chart.js options
  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      title: {
        display: false
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: false
        },
      },
    },
  };

  return <Bar data={chartData} options={options} />;
}


export default ZHVFChart;
