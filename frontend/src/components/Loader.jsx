const Loader = () => {
  return (
    <div style={{ textAlign: "center", marginTop: "20px", color: "var(--primary)" }}>
      {/* Simple CSS Spinner */}
      <div style={{
        display: "inline-block",
        width: "40px",
        height: "40px",
        border: "4px solid rgba(255,255,255,0.1)",
        borderRadius: "50%",
        borderTop: "4px solid var(--primary)",
        animation: "spin 1s linear infinite"
      }}></div>
      <style>{`
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `}</style>
    </div>
  );
};

export default Loader;
