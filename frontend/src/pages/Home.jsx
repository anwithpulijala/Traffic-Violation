import FileUpload from "../components/FileUpload";
import Navbar from "../components/Navbar";

const Home = () => {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar />
      <main className="container" style={{ flex: 1, marginTop: '2rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <h1 style={{
            fontSize: '2.5rem',
            fontWeight: '800',
            marginBottom: '1rem',
            background: 'linear-gradient(to right, white, #94a3b8)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            color: 'transparent'
          }}>
            AI-Powered Helmet & Plate Detection
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', maxWidth: '600px', margin: '0 auto' }}>
            Upload images or videos to automatically detect helmet violations and extract number plates with high accuracy.
          </p>
        </div>

        <FileUpload />
      </main>

      <footer style={{
        textAlign: 'center',
        padding: '2rem',
        color: 'var(--text-secondary)',
        borderTop: '1px solid rgba(148, 163, 184, 0.1)',
        marginTop: 'auto'
      }}>
        <p>&copy; 2024 AI-Based Smart Traffic Violation Detection and Monitoring System. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;
