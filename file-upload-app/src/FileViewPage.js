import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

function FileViewPage() {
  const { fileId } = useParams();
  const [fileContent, setFileContent] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    // Fetch file content by fileId
    axios.get(`http://localhost:8080/file/${fileId}`)
      .then((response) => setFileContent(response.data))
      .catch((error) => {
        console.error("Error fetching file content:", error);
        setError("Error fetching the file content.");
      });
  }, [fileId]);

  return (
    <div className="container my-5">
      <h2>File Content</h2>
      {error && <div className="text-danger">{error}</div>}
      <pre>{fileContent}</pre>
    </div>
  );
}

export default FileViewPage;
