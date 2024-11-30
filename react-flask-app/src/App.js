import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
//import Home from './pages/Home';
import ZHVI from './pages/zhvi';
//import ZORI from './pages/ZORI';
//import ZHVF from './pages/ZHVF';
//import NewConstruction from './pages/NewConstruction';
//import Sales from './pages/Sales';
import './App.css';
function App() {

  return (
    <Router>
      <div className="App">
        <header className="App">
          <h1>Zillow Real Estate Data Dashboard</h1>
        </header>
          <nav>
            <Link to="/zhvi" className="nav-link">Zillow Home Value Index (ZHVI)</Link>
            <Link to="/zhvi" className="nav-link">Zillow Observed Rent Index (ZORI)</Link>
          </nav>
         <main>
          <Routes>
            {/* Define the route for ZHVI */}
            <Route path="/zhvi" element={<ZHVI />} />
          </Routes>
        </main>
      </div>
     </Router>
  );
}

export default App;
