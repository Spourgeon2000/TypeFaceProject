import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./HomePage.js";
import UploadPage from "./UploadPage.js";
import FileViewPage from "./FileViewPage.js";

function App() {
  return (
    <Router>
      <Routes>
        {/* Update component prop to element */}
        <Route path="/" element={<HomePage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/file/:fileId" element={<FileViewPage />} />
      </Routes>
    </Router>
  );
}

export default App;
