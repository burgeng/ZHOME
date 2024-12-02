import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
//import Home from './pages/Home';
import ZHVI from './pages/zhvi';
import ZORI from './pages/zori';
import ZHVF from './pages/zhvf';
import MHI from './pages/mhi'
//import NewConstruction from './pages/NewConstruction';
//import Sales from './pages/Sales';
import './App.css';
function App() {

  const [selectedLocalityType, setSelectedLocalityType] = useState('');

  const handleLocalityTypeSelect = (type) => {
    console.log('Selected locality type:', type); // Debugging
    setSelectedLocalityType(type); // Update selected locality type
  };

  return (
<Router>
      <div className="App">
        <header>
          <h1>Zillow Real Estate Data Dashboard</h1>
          <nav>
            <div className="dropdown">
              <Link to="/zhvi" className="nav-link">Zillow Home Value Index (ZHVI)</Link>
              <div className="dropdown-menu">
                {/* Pass in value of selectedLocalityType */}
                <Link to="/zhvi" onClick={() => handleLocalityTypeSelect('state')}>State</Link>
                <Link to="/zhvi" onClick={() => handleLocalityTypeSelect('metro')}>Metro</Link>
                <Link to="/zhvi" onClick={() => handleLocalityTypeSelect('county')}>County</Link>
                <Link to="/zhvi" onClick={() => handleLocalityTypeSelect('city')}>City</Link>
                <Link to="/zhvi" onClick={() => handleLocalityTypeSelect('zip')}>ZIP</Link>
              </div>
            </div>
            <div className="dropdown">
              <Link to="/zori" className="nav-link">Zillow Observed Rent Index (ZORI)</Link>
              <div className="dropdown-menu">
                <Link to="/zori" onClick={() => handleLocalityTypeSelect('county')}>County</Link>
                <Link to="/zori" onClick={() => handleLocalityTypeSelect('metro')}>Metro</Link>
                <Link to="/zori" onClick={() => handleLocalityTypeSelect('city')}>City</Link>
                <Link to="/zori" onClick={() => handleLocalityTypeSelect('zip')}>ZIP</Link>
              </div>
            </div>
            <div className="dropdown">
              <Link to="/zhvi" className="nav-link">Zillow Home Value Forecast (ZHVF)</Link>
              <div className="dropdown-menu">
                {/* Pass in value of selectedLocalityType */}
                <Link to="/zhvf" onClick={() => handleLocalityTypeSelect('metro')}>Metro</Link>
                <Link to="/zhvf" onClick={() => handleLocalityTypeSelect('zip')}>ZIP</Link>
              </div>
            </div>
            <div className="dropdown">
              <Link to="/zhvi" className="nav-link">Market Heat Index (MHI)</Link>
              <div className="dropdown-menu">
                {/* Pass in value of selectedLocalityType */}
                <Link to="/mhi" onClick={() => handleLocalityTypeSelect('state')}>State</Link>
                <Link to="/mhi" onClick={() => handleLocalityTypeSelect('metro')}>Metro</Link>
              </div>
            </div>
            <div className="dropdown">
              <Link to="/zhvi" className="nav-link">Home Sales</Link>
              <div className="dropdown-menu">
                {/* Pass in value of selectedLocalityType */}
                <Link to="/zhvi" onClick={() => handleLocalityTypeSelect('metro')}>Metro</Link>
              </div>
            </div>
            <div className="dropdown">
              <Link to="/zhvi" className="nav-link">New Construction Sales</Link>
              <div className="dropdown-menu">
                {/* Pass in value of selectedLocalityType */}
                <Link to="/zhvi" onClick={() => handleLocalityTypeSelect('metro')}>Metro</Link>
              </div>
            </div>
            <div className="dropdown">
              <Link to="/zhvi" className="nav-link">For-Sale Listings</Link>
              <div className="dropdown-menu">
                {/* Pass in value of selectedLocalityType */}
                <Link to="/zhvi" onClick={() => handleLocalityTypeSelect('metro')}>Metro</Link>
              </div>
            </div>
          </nav>

        </header>
        <main>
          <Routes>
            {/* Pass selectedLocalityType to ZHVI */}
            <Route path="/zhvi" element={<ZHVI localityType={selectedLocalityType} />} />
            <Route path="/zori" element={<ZORI localityType={selectedLocalityType} />} />
            <Route path="/zhvf" element={<ZHVF localityType={selectedLocalityType} />} />
            <Route path="/mhi" element={<MHI localityType={selectedLocalityType} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
