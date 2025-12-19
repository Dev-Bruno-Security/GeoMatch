import React, { useState, useEffect } from 'react'
import UploadForm from './components/UploadForm'
import ResultsTable from './components/ResultsTable'
import ExportButtons from './components/ExportButtons'

export default function App() {
  const [results, setResults] = useState([])
  const [backendStatus, setBackendStatus] = useState(null)
  // Usar URL relativa em desenvolvimento (proxy), URL completa em produção
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  // Teste de conexão ao backend na montagem do componente
  useEffect(() => {
    console.log('API URL configurada:', apiUrl)
    
    const testUrl = import.meta.env.DEV ? '/api/health' : `${apiUrl}/api/health`
    
    fetch(testUrl)
      .then(res => res.json())
      .then(data => {
        console.log('Backend respondendo:', data)
        setBackendStatus('online')
      })
      .catch(err => {
        console.error('Erro ao conectar ao backend:', err)
        setBackendStatus('offline')
      })
  }, [apiUrl])

  return (
    <div className="app-container">
      <h1>🌍 GeoMatch</h1>
      <p className="subtitle">Normalização, validação e correspondência de endereços.</p>
      
      {backendStatus === 'offline' && (
        <div style={{
          padding: '1rem',
          background: '#fee2e2',
          color: '#991b1b',
          borderRadius: '8px',
          marginBottom: '1rem',
          border: '1px solid #fecaca'
        }}>
          ⚠️ Erro: Backend indisponível. Verifique se o servidor está rodando em http://localhost:8000
        </div>
      )}
      
      {backendStatus === 'online' && (
        <div style={{
          padding: '0.5rem 1rem',
          background: '#dbeafe',
          color: '#1e40af',
          borderRadius: '8px',
          marginBottom: '1rem',
          fontSize: '0.9em',
          border: '1px solid #93c5fd'
        }}>
          ✓ Backend conectado
        </div>
      )}

      <UploadForm onResults={setResults} apiUrl={apiUrl} />

      {results.length > 0 && (
        <>
          <h2 style={{ marginTop: '2rem', color: '#333' }}>📊 Resultados</h2>
          <ResultsTable rows={results} />
          <ExportButtons apiUrl={apiUrl} />
        </>
      )}
    </div>
  )
}
