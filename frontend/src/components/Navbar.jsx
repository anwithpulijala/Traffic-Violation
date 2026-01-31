import React from 'react';

const Navbar = () => {
  return (
    <nav style={{
      position: 'sticky',
      top: 0,
      zIndex: 50,
      backdropFilter: 'blur(12px)',
      backgroundColor: 'rgba(15, 23, 42, 0.8)',
      borderBottom: '1px solid rgba(148, 163, 184, 0.1)',
      padding: '1rem 2rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div style={{
          width: '32px',
          height: '32px',
          background: 'linear-gradient(135deg, var(--primary), var(--accent))',
          borderRadius: '8px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 'bold',
          color: 'white'
        }}>
          AI
        </div>
        <h2 style={{
          fontSize: '1rem',
          fontWeight: '700',
          margin: 0,
          background: 'linear-gradient(to right, #fff, #94a3b8)',
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          color: 'transparent',
          lineHeight: '1.4'
        }}>
          AI-Based Smart Traffic Violation Detection and Monitoring System
        </h2>
      </div>

      {/* Optional: Add links or actions here */}
      <div style={{ display: 'flex', gap: '1rem' }}>
        {/* Could add a 'GitHub' link or similar here */}
      </div>
    </nav>
  );
};

export default Navbar;



