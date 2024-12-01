import React, { useState } from 'react';

function ZORI({ localityType }) {
  const [localityName, setLocalityName] = useState(''); // User input for locality name
  const [submittedLocality, setSubmittedLocality] = useState(''); // Stores the submitted locality
  const [error, setError] = useState(null); // Error handling
  const [data, setData] = useState(null); // Data fetched for the locality

  // Handle input change
  const handleInputChange = (event) => {
    setLocalityName(event.target.value); // Update the locality name as the user types
  };

  // Handle form submission
  const handleSubmit = () => {
    if (localityName.trim() === '') {
      setError('Please enter a valid locality name.');
      return;
    }
    setSubmittedLocality(localityName); // Save the submitted locality name
    setError(null); // Clear previous errors
    setData(null); // Clear previous data

    // Simulate fetching data for the entered locality
    //const route = `get_localities_zhvi?type=${localityType}`;
    const route = `get_zori?type=${localityType}&name='${localityName}'`;
    fetch(route)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`No data found for ${localityName} in ${localityType}`);
        }
        return response.json();
      })
      .then((result) => setData(result))
      .catch((err) => setError(err.message));
  };

  return (
    <div>
      <h2>Zillow Observed Rent Index (ZORI)</h2>

      {/* Display the selected locality type */}
      {localityType && <p>You selected locality type: <strong>{localityType}</strong></p>}

      {/* Textbox for entering locality name */}
      {localityType && (
        <div style={{ marginTop: '20px' }}>
          <label htmlFor="localityInput">
            Enter the name of the {localityType}:
          </label>
          <input
            id="localityInput"
            type="text"
            value={localityName}
            onChange={handleInputChange}
            placeholder={`Enter ${localityType} name`}
            style={{ marginLeft: '10px', padding: '5px', fontSize: '1rem' }}
          />
          <button
            onClick={handleSubmit}
            style={{
              marginLeft: '10px',
              padding: '5px 10px',
              fontSize: '1rem',
              cursor: 'pointer',
            }}
          >
            Search
          </button>
        </div>
      )}

      {/* Error message */}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* Display the fetched data */}
      {submittedLocality && data && (
        <div style={{ marginTop: '20px' }}>
          <h3>Results for {submittedLocality}:</h3>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}

      {/* Show a loading message while fetching data */}
      {submittedLocality && !data && !error && (
        <p>Fetching data for <strong>{submittedLocality}</strong>...</p>
      )}
    </div>
  );
}

export default ZORI;
