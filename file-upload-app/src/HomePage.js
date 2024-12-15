import React, { useState, useEffect } from "react";
import axios from "axios";
import './HomePage.css';  // Custom styles for UI

function HomePage() {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    // Fetch the list of files from the server
    axios.get("http://localhost:8080/file/")
      .then((response) => setFiles(response.data))
      .catch((error) => console.error("Error fetching files:", error));
  }, []);

  const handleDownload = (fileId) => {
    // Logic to handle file download
    const url = `http://localhost:8080/file/${fileId}`;
    window.location.href = url;
  };

  return (
    <div className="container my-5">
      <div className="header text-center mb-5">
        <h2>File Management System</h2>
      </div>
      
      {/* Upload Button */}
      <div className="upload-btn-container">
        <button className="upload-btn" onClick={() => window.location.href = "/upload"}>
          Upload New File
        </button>
      </div>

      {/* File Display Section */}
      <div className="file-card-container">
        {files.map((file) => (
          <div className="file-card card" key={file.id}>
            <div className="card-body">
              <p className="file-name">{file.fileName}</p>
              <p className="uploaded-by">Uploaded by: {file.userId}</p>
              <button
                className="download-btn"
                onClick={() => handleDownload(file.id)}
              >
                Download
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <footer>
        <p>&copy; 2024 File Management System Made By Joseph</p>
      </footer>
    </div>
  );
}

export default HomePage;
