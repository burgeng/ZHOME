
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

function ZORIChart({ data }) {
  if (!data || !data.length) {
    return <p>No data to display.</p>;
  }

  // Build labels and values safely
  const labels = data.map(item =>
    new Date(item.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short' })
  );
  const zoriValues = data.map(item =>
    parseFloat(item.ZORI ?? item.zori ?? 0)
  );

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Zillow Observed Rent Index (ZORI)',
        data: zoriValues,
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
      title: { display: true, text: 'ZORI Trend' },
      tooltip: {
        callbacks: {
          label: (context) => {
            const val = context.parsed.y;
            return `ZORI: ${val.toLocaleString()}`;
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
        title: { display: true, text: 'ZORI (USD)' },
      },
    },
  };

  return <Line data={chartData} options={options} />;
}

export default ZORIChart;

