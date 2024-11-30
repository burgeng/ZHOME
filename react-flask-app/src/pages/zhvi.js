import React, { useState, useEffect } from 'react';

function ZHVI() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

    useEffect(() => {
    fetch('/get_mean_zhvi_by_metro')
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => setError(error.message));
  }, []);


  return (
    <div>
      <h2>ZHVI Data</h2>
    </div>
  );
}

export default ZHVI;