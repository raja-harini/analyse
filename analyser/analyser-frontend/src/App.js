import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import AccountAnalysis from "./analyser"; // Assuming analyser.js is in the same folder
import "./App.css";

function App() {
  const [transactions, setTransactions] = useState([]);
  const [error, setError] = useState("");

  const analyzeFile = async (fileName) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_name: fileName }),
      });

      const result = await response.json();
      if (response.ok) {
        setTransactions(result.transactions);
      } else {
        setError(result.error || "Error analyzing file");
      }
    } catch (err) {
      setError("Failed to analyze file.");
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Upload File</h1>
        <UploadForm onAnalyze={analyzeFile} />
        <AccountAnalysis transactions={transactions} />
        {error && <p style={{ color: "red" }}>{error}</p>}
      </header>
    </div>
  );
}

export default App;