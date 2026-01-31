import { useState, useRef } from "react";
import { detectFile } from "../services/api";
import Loader from "./Loader";
import ResultCard from "./ResultCard";

const FileUpload = () => {
  const [files, setFiles] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFiles = (selectedFiles) => {
    if (selectedFiles && selectedFiles.length > 0) {
      setFiles(selectedFiles);
    }
  };

  const onDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    handleFiles(e.dataTransfer.files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!files) return;

    setLoading(true);
    setResults([]);

    try {
      const data = await detectFile(files);
      // Ensure data is array (backend now returns list)
      setResults(Array.isArray(data) ? data : [data]);
    } catch (err) {
      console.error("Full error object:", err);
      const errorMsg = `
        Error: ${err.message}
        Code: ${err.code}
        URL: ${err.config?.url}
        Status: ${err.response?.status}
        Data: ${JSON.stringify(err.response?.data)}
      `;
      alert("Detection Failure Details:\n" + errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} style={{ maxWidth: '600px', margin: '0 auto 3rem' }}>
        <div
          className={`upload-zone ${isDragging ? 'active' : ''}`}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onDrop={onDrop}
          onClick={() => fileInputRef.current.click()}
        >
          <input
            type="file"
            multiple
            accept="image/*,video/*"
            onChange={(e) => handleFiles(e.target.files)}
            style={{ display: 'none' }}
            ref={fileInputRef}
          />

          <div style={{ pointerEvents: 'none' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📂</div>
            <h3 style={{ margin: '0 0 0.5rem', color: 'var(--text-primary)' }}>
              {files ? `${files.length} file(s) selected` : "Drag files here or click to browse"}
            </h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>
              Supports Images (JPG, PNG) and Videos (MP4, WebM)
            </p>
            {files && (
              <div style={{ marginTop: '1rem', color: 'var(--primary)', fontWeight: '500' }}>
                Ready to process
              </div>
            )}
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={!files || loading}
            style={{ minWidth: '200px', fontSize: '1.1rem' }}
          >
            {loading ? 'Processing...' : 'Run Detection'}
          </button>
        </div>
      </form>

      {loading && <Loader />}

      {results.length > 0 && (
        <div className="result-card-container">
          {results.map((res, index) => (
            <ResultCard key={index} result={res} />
          ))}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
