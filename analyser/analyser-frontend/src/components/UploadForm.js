import React, { useState } from "react";

const UploadForm = ({ onAnalyze }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState("");
  const [uploadedFileName, setUploadedFileName] = useState("");

  const handleFileChange = (event) => {
    if (event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
      setUploadedFileName("");
      setMessage("");
    }
  };

  const uploadFile = async () => {
    if (!selectedFile) {
      alert("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/upload/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "File upload failed");
      }

      setMessage("File uploaded successfully: " + data.file_url);
      setUploadedFileName(selectedFile.name); // Store uploaded file name
      console.log("✅ Uploaded File Name:", selectedFile.name); // Debugging
    } catch (error) {
      console.error("🚨 Upload error:", error);
      setMessage("Error uploading file: " + error.message);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Account Statement</h2>
      <input type="file" accept=".pdf,.jpg,.png" onChange={handleFileChange} />
      <button onClick={uploadFile}>Upload</button>
      {uploadedFileName && (
        <button onClick={() => onAnalyze(uploadedFileName)}>Analyze</button>
      )}
      {message && <p>{message}</p>}
    </div>
  );
};

export default UploadForm;
