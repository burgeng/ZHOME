//
import React, { useState } from 'react'; // State handling
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'; // Routing
//
import ZHVI from './pages/zhvi';
import ZORI from './pages/zori';
import ZHVF from './pages/zhvf';
import MHI from './pages/mhi';
import HomeSales from './pages/homesales'
import NewConstruction from './pages/newConstructionSales';
import './App.css';

// The main functional component
function App() {

  const [selectedLocalityType, setSelectedLocalityType] = useState(''); // React hook, adds a state variable to the component

  // Event handler 
  const handleLocalityTypeSelect = (type) => {
    console.log('Selected locality type:', type); // Print for debugging 
    setSelectedLocalityType(type); // Handle event: update the selected locality type (function defined above with useState() definition)
  };

  return ( // HTML to return
<Router> {/* Wrap the page with BrowserRouter to enable routing */}
      <div className="App">
        <header>
          <h1>Zillow Real Estate Data Dashboard</h1>
          <nav>
            <div className="dropdown"> {/*GROUP THE NAV ITEM AND THE SUBMENU*/}
              <Link to="/zhvi" className="nav-link">Zillow Home Value Index (ZHVI)</Link>
              <div className="dropdown-menu"> {/*Hold the clickaBLE OPTIONS*/}
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
              <Link to="/mhi" className="nav-link">Market Heat Index (MHI)</Link>
              <div className="dropdown-menu">
                <Link to="/mhi" onClick={() => handleLocalityTypeSelect('state')}>State</Link>
                <Link to="/mhi" onClick={() => handleLocalityTypeSelect('metro')}>Metro</Link>
              </div>
            </div>
            <div className="dropdown">
              <Link to="/newConstructionSales" className="nav-link">New Construction Sales</Link>
              <div className="dropdown-menu">
                {/* Pass in value of selectedLocalityType */}
                <Link to="/newConstructionSales" onClick={() => handleLocalityTypeSelect('metro')}>Metro</Link>
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
          {/* Map paths to imported React components*/}
          {/* Also pass the selectedLocalityType to the components*/}
          {/* Defines which page component renders for each path*/}
          {/* Decide which child component to render (pages app can show, main page content) */}
          <Routes>
            {/* Pass selectedLocalityType to each component function */}
            <Route path="/zhvi" element={<ZHVI localityType={selectedLocalityType} />} /> 
            <Route path="/zori" element={<ZORI localityType={selectedLocalityType} />} />
            <Route path="/zhvf" element={<ZHVF localityType={selectedLocalityType} />} />
            <Route path="/mhi" element={<MHI localityType={selectedLocalityType} />} />
            <Route path="/homesales" element={<HomeSales localityType={selectedLocalityType} />} />
            <Route path="/newConstructionSales" element={<NewConstruction localityType={selectedLocalityType} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
