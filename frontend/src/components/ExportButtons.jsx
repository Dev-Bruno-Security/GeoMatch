import React from 'react'

export default function ExportButtons({ apiUrl }) {
  const getApiUrl = () => {
    // Em desenvolvimento, usar URL relativa (proxy)
    // Em produção, usar a URL completa
    return import.meta.env.DEV ? '' : apiUrl
  }

  const handleExport = (format) => {
    const baseUrl = getApiUrl()
    window.open(`${baseUrl}/api/export/${format}`, '_blank')
  }

  const buttonStyle = {
    padding: '0.75rem 1.5rem',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '1rem',
    fontWeight: '500',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    transition: 'all 0.2s ease',
    textDecoration: 'none',
    color: 'white'
  }

  const csvStyle = {
    ...buttonStyle,
    background: 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)',
  }

  const sqlStyle = {
    ...buttonStyle,
    background: 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)',
  }

  return (
    <div style={{ 
      marginTop: '1.5rem', 
      display: 'flex', 
      gap: '1rem',
      flexWrap: 'wrap',
      padding: '1rem',
      background: '#f9f9f9',
      borderRadius: '8px',
      border: '1px solid #e0e0e0'
    }}>
      <button 
        onClick={() => handleExport('csv')}
        style={csvStyle}
        onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
        onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
      >
        <span>📥</span>
        <span>Exportar CSV</span>
      </button>
      
      <button 
        onClick={() => handleExport('sql')}
        style={sqlStyle}
        onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
        onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
      >
        <span>📥</span>
        <span>Exportar SQL</span>
      </button>
      
      <div style={{ 
        marginLeft: 'auto', 
        display: 'flex', 
        alignItems: 'center', 
        color: '#666',
        fontSize: '0.9rem'
      }}>
        <span>💡 Exporta todos os resultados processados</span>
      </div>
    </div>
  )
}
