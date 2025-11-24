import React from 'react';
import { Link } from 'react-router-dom';
import { LogoIcon } from './Icons.tsx';

const Landing: React.FC = () => {
  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-app)', color: 'var(--text-primary)', position: 'relative', overflow: 'hidden' }}>
      {/* Navbar */}
      <nav style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        background: 'rgba(0, 0, 0, 0.8)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid var(--color-border)',
        padding: '10px 20px',
        zIndex: 1000,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', color: 'var(--color-accent)' }}>
          <LogoIcon />
          <span style={{ marginLeft: '10px', fontWeight: 'bold' }}>MCP SERVER HUB</span>
        </div>
        <div style={{ display: 'flex', gap: '20px' }}>
          <a href="#home" style={{ color: 'var(--text-primary)', textDecoration: 'none', transition: 'color 0.3s', position: 'relative' }}
             onMouseEnter={(e) => e.currentTarget.style.color = 'var(--color-accent)'}
             onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-primary)'}>Home</a>
          <a href="#features" style={{ color: 'var(--text-primary)', textDecoration: 'none', transition: 'color 0.3s', position: 'relative' }}
             onMouseEnter={(e) => e.currentTarget.style.color = 'var(--color-accent)'}
             onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-primary)'}>Features</a>
          <a href="#about" style={{ color: 'var(--text-primary)', textDecoration: 'none', transition: 'color 0.3s', position: 'relative' }}
             onMouseEnter={(e) => e.currentTarget.style.color = 'var(--color-accent)'}
             onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-primary)'}>About</a>
          <Link to="/login" style={{ color: 'var(--color-accent)', textDecoration: 'none', fontWeight: 'bold', transition: 'all 0.3s', position: 'relative' }}
                onMouseEnter={(e) => { e.currentTarget.style.color = 'white'; e.currentTarget.style.transform = 'scale(1.05)'; }}
                onMouseLeave={(e) => { e.currentTarget.style.color = 'var(--color-accent)'; e.currentTarget.style.transform = 'scale(1)'; }}>Login</Link>
        </div>
      </nav>

      <div style={{ paddingTop: '80px' }}> {/* Offset for fixed navbar */}
        <header id="home" style={{ textAlign: 'center', padding: '60px 20px', position: 'relative', zIndex: 1 }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px', color: 'var(--color-accent)' }}>
            <LogoIcon />
          </div>
          <h1 style={{
            fontSize: '48px',
            fontWeight: '600',
            marginBottom: '16px',
            animation: 'fadeInUp 1s ease-out'
          }}>MCP SERVER HUB</h1>
          <p style={{
            fontSize: '18px',
            color: 'var(--text-secondary)',
            animation: 'fadeInUp 1s ease-out 0.2s both'
          }}>A powerful platform for managing and deploying MCP servers</p>
          <Link to="/signup" style={{
            display: 'inline-block',
            marginTop: '20px',
            padding: '12px 24px',
            background: 'var(--color-accent)',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '8px',
            fontWeight: 'bold',
            transition: 'all 0.3s',
            animation: 'fadeInUp 1s ease-out 0.4s both'
          }}>Get Started</Link>
        </header>

        <WorkflowAnimation />

        <section id="features" style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px', position: 'relative', zIndex: 1 }}>
          <h2 style={{
            fontSize: '32px',
            marginBottom: '40px',
            textAlign: 'center',
            animation: 'fadeInUp 1s ease-out'
          }}>Use Cases</h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '30px',
            animation: 'fadeInUp 1s ease-out 0.2s both'
          }}>
            <div style={{
              padding: '30px',
              background: 'var(--bg-surface)',
              borderRadius: '12px',
              boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
              transition: 'transform 0.3s, box-shadow 0.3s',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-5px)';
              e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.2)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
            }}>
              <h3 style={{ color: 'var(--color-accent)', marginBottom: '10px' }}>Server Management</h3>
              <p>Easily deploy and manage multiple MCP servers from a single interface.</p>
            </div>
            <div style={{
              padding: '30px',
              background: 'var(--bg-surface)',
              borderRadius: '12px',
              boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
              transition: 'transform 0.3s, box-shadow 0.3s',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-5px)';
              e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.2)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
            }}>
              <h3 style={{ color: 'var(--color-accent)', marginBottom: '10px' }}>Real-time Monitoring</h3>
              <p>Monitor server performance, logs, and health in real-time.</p>
            </div>
            <div style={{
              padding: '30px',
              background: 'var(--bg-surface)',
              borderRadius: '12px',
              boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
              transition: 'transform 0.3s, box-shadow 0.3s',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-5px)';
              e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.2)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
            }}>
              <h3 style={{ color: 'var(--color-accent)', marginBottom: '10px' }}>Scalable Architecture</h3>
              <p>Built with modern technologies for high scalability and reliability.</p>
            </div>
          </div>
        </section>

        <section id="about" style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px', position: 'relative', zIndex: 1 }}>
          <h2 style={{
            fontSize: '32px',
            marginBottom: '40px',
            textAlign: 'center',
            animation: 'fadeInUp 1s ease-out'
          }}>Technical Features</h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '30px',
            animation: 'fadeInUp 1s ease-out 0.2s both'
          }}>
            <div style={{
              padding: '25px',
              background: 'var(--bg-surface)',
              borderRadius: '12px',
              boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
              transition: 'transform 0.3s',
              textAlign: 'center'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}>
              <h3 style={{ color: 'var(--color-accent)', marginBottom: '10px' }}>React Frontend</h3>
              <p>Modern, responsive UI built with React and styled components.</p>
            </div>
            <div style={{
              padding: '25px',
              background: 'var(--bg-surface)',
              borderRadius: '12px',
              boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
              transition: 'transform 0.3s',
              textAlign: 'center'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}>
              <h3 style={{ color: 'var(--color-accent)', marginBottom: '10px' }}>Express Backend</h3>
              <p>Robust API server with authentication and data management.</p>
            </div>
            <div style={{
              padding: '25px',
              background: 'var(--bg-surface)',
              borderRadius: '12px',
              boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
              transition: 'transform 0.3s',
              textAlign: 'center'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}>
              <h3 style={{ color: 'var(--color-accent)', marginBottom: '10px' }}>MongoDB Database</h3>
              <p>NoSQL database for flexible and scalable data storage.</p>
            </div>
            <div style={{
              padding: '25px',
              background: 'var(--bg-surface)',
              borderRadius: '12px',
              boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
              transition: 'transform 0.3s',
              textAlign: 'center'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}>
              <h3 style={{ color: 'var(--color-accent)', marginBottom: '10px' }}>JWT Authentication</h3>
              <p>Secure user authentication with JSON Web Tokens.</p>
            </div>
          </div>
        </section>

        <footer style={{
          textAlign: 'center',
          padding: '40px 20px',
          color: 'var(--text-muted)',
          position: 'relative',
          zIndex: 1,
          animation: 'fadeInUp 1s ease-out'
        }}>
          <p>&copy; 2025 MCP Server Hub. All rights reserved.</p>
        </footer>
      </div>
    </div>
  );
};

const WorkflowAnimation = () => {
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 0 }}>
      {/* Floating particles */}
      {Array.from({ length: 20 }, (_, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            width: `${Math.random() * 6 + 2}px`,
            height: `${Math.random() * 6 + 2}px`,
            background: 'var(--color-accent)',
            borderRadius: '50%',
            opacity: Math.random() * 0.5 + 0.2,
            animation: `float ${Math.random() * 10 + 10}s linear infinite`,
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 10}s`
          }}
        />
      ))}

      {/* Morphing shapes */}
      <div style={{
        position: 'absolute',
        top: '15%',
        left: '10%',
        width: '80px',
        height: '80px',
        background: 'linear-gradient(45deg, var(--color-accent), transparent)',
        borderRadius: '50%',
        animation: 'morph 8s ease-in-out infinite',
        opacity: 0.3
      }}></div>
      <div style={{
        position: 'absolute',
        top: '25%',
        right: '15%',
        width: '60px',
        height: '60px',
        background: 'linear-gradient(45deg, var(--color-accent), transparent)',
        borderRadius: '20%',
        animation: 'morph-reverse 10s ease-in-out infinite',
        opacity: 0.3
      }}></div>
      <div style={{
        position: 'absolute',
        bottom: '20%',
        left: '20%',
        width: '100px',
        height: '100px',
        background: 'linear-gradient(45deg, var(--color-accent), transparent)',
        borderRadius: '30%',
        animation: 'morph 12s ease-in-out infinite',
        opacity: 0.2
      }}></div>

      {/* Animated connections */}
      <svg width="100%" height="100%" style={{ position: 'absolute', top: 0, left: 0 }}>
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="var(--color-accent)" stopOpacity="0.1" />
            <stop offset="50%" stopColor="var(--color-accent)" stopOpacity="0.5" />
            <stop offset="100%" stopColor="var(--color-accent)" stopOpacity="0.1" />
          </linearGradient>
        </defs>
        <path d="M 10% 20% Q 50% 10% 90% 30%" stroke="url(#gradient)" strokeWidth="3" fill="none">
          <animate attributeName="stroke-dasharray" values="0,100;100,0" dur="4s" repeatCount="indefinite" />
        </path>
        <path d="M 20% 60% Q 60% 80% 80% 50%" stroke="url(#gradient)" strokeWidth="2" fill="none">
          <animate attributeName="stroke-dasharray" values="0,100;100,0" dur="6s" repeatCount="indefinite" />
        </path>
        <path d="M 5% 80% Q 40% 60% 95% 85%" stroke="url(#gradient)" strokeWidth="2" fill="none">
          <animate attributeName="stroke-dasharray" values="0,100;100,0" dur="8s" repeatCount="indefinite" />
        </path>
      </svg>

      {/* Pulsing nodes */}
      <div style={{
        position: 'absolute',
        top: '30%',
        left: '15%',
        width: '20px',
        height: '20px',
        background: 'var(--color-accent)',
        borderRadius: '50%',
        animation: 'pulse 2s ease-in-out infinite'
      }}></div>
      <div style={{
        position: 'absolute',
        top: '50%',
        right: '25%',
        width: '15px',
        height: '15px',
        background: 'var(--color-accent)',
        borderRadius: '50%',
        animation: 'pulse 3s ease-in-out infinite',
        animationDelay: '1s'
      }}></div>
      <div style={{
        position: 'absolute',
        bottom: '30%',
        left: '40%',
        width: '25px',
        height: '25px',
        background: 'var(--color-accent)',
        borderRadius: '50%',
        animation: 'pulse 2.5s ease-in-out infinite',
        animationDelay: '0.5s'
      }}></div>
    </div>
  );
};

// Add CSS for animations
const styles = `
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
@keyframes rotate-reverse {
  from { transform: rotate(360deg); }
  to { transform: rotate(0deg); }
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes float {
  0% { transform: translateY(0px) translateX(0px); }
  33% { transform: translateY(-20px) translateX(10px); }
  66% { transform: translateY(10px) translateX(-10px); }
  100% { transform: translateY(0px) translateX(0px); }
}
@keyframes morph {
  0%, 100% { border-radius: 50%; transform: scale(1); }
  25% { border-radius: 20%; transform: scale(1.1); }
  50% { border-radius: 30%; transform: scale(0.9); }
  75% { border-radius: 40%; transform: scale(1.05); }
}
@keyframes morph-reverse {
  0%, 100% { border-radius: 20%; transform: scale(1); }
  25% { border-radius: 40%; transform: scale(1.1); }
  50% { border-radius: 50%; transform: scale(0.9); }
  75% { border-radius: 30%; transform: scale(1.05); }
}
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.2); opacity: 1; }
}
`;

// Inject styles
const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = styles;
document.head.appendChild(styleSheet);

export default Landing;