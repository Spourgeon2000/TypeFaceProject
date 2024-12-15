import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // React Router v6
import './UploadPage.css'; // Custom styling

function UploadPage() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [userId, setUserId] = useState(""); // State for userId
  const navigate = useNavigate(); // Use navigate instead of useHistory

  const allowedTypes = ["text/plain", "image/jpeg", "image/png", "application/json", "application/pdf"];

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && allowedTypes.includes(selectedFile.type)) {
      setFile(selectedFile);
      setError(""); // Reset error if file is valid
    } else {
      setFile(null);
      setError("Invalid file type. Only txt, jpg, png, pdf, json files are allowed.");
    }
  };

  const handleUpload = () => {
    if (file && userId) {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("userId", userId); // Use userId from input field

      // API call to upload the file
      axios.post("http://localhost:8080/file/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
        .then(() => {
          setSuccess("File uploaded successfully!");
          setError(""); // Clear any previous error message
          navigate("/"); // Redirect to home page after successful upload
        })
        .catch((error) => {
          console.error("File upload error:", error);
          setError("Error uploading the file.");
          setSuccess(""); // Clear success message in case of error
        });
    } else {
      setError("Please provide both a file and userId.");
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-header">
        <h2>Upload Your File</h2>
        <p className="subheading">Please enter your name and choose the file to upload.</p>
      </div>

      <div className="upload-card">
        <div className="form-group">
          {/* Input for userId */}
          <label htmlFor="userId" className="label-text">Please Enter Your Name Below</label>
          <input
            id="userId"
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)} // Update userId state
            className="form-control"
            placeholder="Enter your Name"
          />
        </div>

        <div className="form-group">
  {/* File input */}
  <label htmlFor="file" className="file-upload-label-text">Choose a File to Upload</label>
  <div className="custom-file-upload">
    <input
      id="file"
      type="file"
      onChange={handleFileChange}
      className="upload-input"
    />
    <label className={`file-upload-label ${file ? "file-chosen" : ""}`}>
      {file ? file.name : "Click on Choose a File to Upload Above"}
    </label>
  </div>
</div>


        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <div className="upload-btn-container">
          <button onClick={handleUpload} className="upload-btn">
            Upload
          </button>
        </div>
      </div>
    </div>
  );
}

export default UploadPage;
