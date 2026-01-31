const ResultCard = ({ result }) => {
  if (!result) return null;

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h4 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--text-primary)' }}>
          {result.filename}
        </h4>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '8px' }}>
          <span style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Helmet Status</span>
          <span style={{ fontWeight: '600', color: result.helmet === "YES" ? 'var(--success)' : result.helmet === "NO" ? 'var(--danger)' : 'var(--text-secondary)' }}>
            {result.helmet === "YES" ? "DETECTED" : result.helmet === "NO" ? "NOT DETECTED" : "UNKNOWN"}
          </span>
        </div>

        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '8px' }}>
          <span style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Number Plate Status</span>
          <span style={{ fontWeight: '600', color: result.number_plate === "DETECTED" ? 'var(--success)' : 'var(--text-secondary)' }}>
            {result.number_plate}
          </span>
        </div>

        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '8px' }}>
          <span style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Extracted Number</span>
          <span style={{ fontWeight: '600', fontFamily: 'monospace', fontSize: '1.1rem', letterSpacing: '1px' }}>
            {result.plate_number || "N/A"}
          </span>
        </div>
      </div>

      {result.output_file && (
        <div className="output-image-container">
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>Processed Visual Output:</p>
          {/* Robustly handle path: replace backslashes, remove 'outputs/' prefix if present */}
          {(() => {
            const filename = result.output_file.replace(/\\/g, "/").split('/').pop();
            const isVideo = filename.match(/\.(mp4|avi|mov|mkv|webm)$/i);

            // If output_file is already a http URL, use it; otherwise use local proxy
            const fileUrl = result.output_file.startsWith("http")
              ? result.output_file
              : `http://127.0.0.1:8000/outputs/${filename}`;

            if (isVideo) {
              return (
                <video
                  controls
                  style={{ width: "100%", borderRadius: "8px", border: "1px solid rgba(148, 163, 184, 0.2)" }}
                >
                  <source src={fileUrl} type="video/webm" />
                  <source src={fileUrl} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              );
            } else {
              return (
                <a href={fileUrl} target="_blank" rel="noopener noreferrer" style={{ display: 'block', cursor: 'pointer' }}>
                  <img
                    src={fileUrl}
                    alt="Detection Result"
                    style={{ width: "100%", borderRadius: "8px", border: "1px solid rgba(148, 163, 184, 0.2)" }}
                    onError={(e) => {
                      console.error("Image load failed:", e.target.src);
                      e.target.style.display = 'none';
                      // Avoid alerting endlessly if many fail
                    }}
                  />
                </a>
              );
            }
          })()}
        </div>
      )}
    </div>
  );
};

export default ResultCard;
