import React, { useState, useEffect } from 'react';
import MHIChart from './mhichart'; // Import the chart component

function MHI({ localityType }) {
  const [localityOptions, setLocalityOptions] = useState([]); // List of locality options
  const [selectedLocality, setSelectedLocality] = useState(null); // User-selected locality (object with regionname and state)
  const [error, setError] = useState(null); // Error handling
  const [currentPage, setCurrentPage] = useState(1); // Current page
  const [totalPages, setTotalPages] = useState(0); // Total pages
  const [data, setData] = useState(null); // Data for the plot
  const optionsPerPage = 10; // Number of options per page

  // Fetch locality options for the current page
  useEffect(() => {
    if (localityType) {
      setError(null);
      const route = `/get_localities_mhi?type=${localityType}&page=${currentPage}&limit=${optionsPerPage}`;
      fetch(route)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Failed to fetch options for ${localityType}`);
          }
          return response.json();
        })
        .then((result) => {
          setLocalityOptions(result.options); // Update options for the current page
          setTotalPages(result.totalPages); // Update total pages
        })
        .catch((err) => setError(err.message));
    }
  }, [localityType, currentPage]);

  // Handle page change
  const handlePageChange = (direction) => {
    if (direction === 'next' && currentPage < totalPages) {
      setCurrentPage((prev) => prev + 1);
    } else if (direction === 'prev' && currentPage > 1) {
      setCurrentPage((prev) => prev - 1);
    }
  };

  // Fetch data for the selected locality
  const fetchDataForLocality = (locality) => {
    setError(null);
    setSelectedLocality(locality);
    setData(null); // Clear previous data
    const route = `/get_mhi?type=${localityType}&name=${encodeURIComponent(locality.regionname)}`;
    fetch(route)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`No data found for ${locality.regionname}, ${locality.state}`);
        }
        return response.json();
      })
      .then((result) => setData(result))
      .catch((err) => setError(err.message));
  };

  return (
    <div>
      <h2>Market Heat Index (MHI)</h2>

      {/* Display the selected locality type */}
      {localityType && <p>You selected locality type: <strong>{localityType}</strong></p>}

      {/* Error message */}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* No options available */}
      {localityType && localityOptions.length === 0 && !error && (
        <p>Fetching {localityType} options...</p>
      )}

      {/* Display table with clickable options */}
      {localityType && localityOptions.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ border: '1px solid #ccc', padding: '10px' }}>Region</th>
              </tr>
            </thead>
            <tbody>
              {localityOptions.map((option, index) => (
                <tr
                  key={index}
                  onClick={() => fetchDataForLocality(option)}
                  style={{ cursor: 'pointer', backgroundColor: '#f9f9f9' }}
                  onMouseEnter={(e) => (e.target.style.backgroundColor = '#e0e0e0')}
                  onMouseLeave={(e) => (e.target.style.backgroundColor = '#f9f9f9')}
                >
                  <td style={{ border: '1px solid #ccc', padding: '10px' }}>
                    {`${option.regionname}, ${option.state}`}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'space-between' }}>
            <button
              onClick={() => handlePageChange('prev')}
              disabled={currentPage === 1}
              style={{ padding: '10px', cursor: currentPage === 1 ? 'not-allowed' : 'pointer' }}
            >
              Previous
            </button>
            <span>
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => handlePageChange('next')}
              disabled={currentPage === totalPages}
              style={{
                padding: '10px',
                cursor: currentPage === totalPages ? 'not-allowed' : 'pointer',
              }}
            >
              Next
            </button>
          </div>
        </div>
      )}

      {/* Display plot if data is available */}
      {selectedLocality && data && (
        <div style={{ marginTop: '20px' }}>
          <h3>MHI for {selectedLocality.regionname}, {selectedLocality.state}:</h3>
          <MHIChart data={data} />
          <h4>*The by-state data has been estimated by averaging the MHI for all metros within a state.</h4>
        </div>
      )}

      {/* Show a loading message while fetching data */}
      {selectedLocality && !data && !error && (
        <p>Loading data for <strong>{selectedLocality.regionname}, {selectedLocality.state}</strong>...</p>
      )}
    </div>
  );
}

export default MHI;
