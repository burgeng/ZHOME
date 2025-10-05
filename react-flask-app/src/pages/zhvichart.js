// src/pages/zhvichart.js
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

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function ZHVIChart({ data }) {
  if (!data || !data.length) {
    return <p>No data to display.</p>;
  }

  // Build labels and values safely
  const labels = data.map(item =>
    new Date(item.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short' })
  );
  const zhviValues = data.map(item =>
    parseFloat(item.ZHVI ?? item.zhvi ?? 0)
  );

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Zillow Home Value Index (ZHVI)',
        data: zhviValues,
        fill: false,
        borderColor: 'darkblue',
        tension: 0.3,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'ZHVI Trend' },
      tooltip: {
        callbacks: {
          label: (context) => {
            const val = context.parsed.y;
            return `ZHVI: ${val.toLocaleString()}`;
          },
        },
      },
    },
    scales: {
      x: {
        title: { display: true, text: 'Date' },
        ticks: { maxTicksLimit: 12 },
      },
      y: {
        title: { display: true, text: 'ZHVI (USD)' },
      },
    },
  };

  return <Line data={chartData} options={options} />;
}

export default ZHVIChart;
