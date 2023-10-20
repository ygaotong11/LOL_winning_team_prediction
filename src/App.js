import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({ name: '' });
  const [jsonData, setJsonData] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null); // Define the state variable


  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Need to replace per 24 hours
    const api_key = 'RGAPI-a32340f1-8465-4b0f-b61f-87c1d4c8b2b4'; 

    // Construct the URL with the formData.name as the apiKey parameter
    const apiUrl = `https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/${formData.name}?api_key=${api_key}`;


    try {
        const response = await fetch(apiUrl, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });

        const data = await response.json();
        setJsonData(data);
        setErrorMessage(null); // Clear any previous error messages

      // If you need to use a callback after setting state:
      // callback(data);

      } catch (error) {
          setErrorMessage("ID does not exist"); // Set the error message in state
          console.error('EXCEPTION:', error);
      }
    };

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ name: e.target.value })}
          placeholder="Enter a Summoner name"
        />
        <button type="submit">Search</button>
      </form>

      {errorMessage ? (
            <p>{errorMessage}</p>
        ) : (
            jsonData && <pre>{JSON.stringify(jsonData, null, 2)}</pre>
        )}
      
        
    </div>
  );
}

export default App;




