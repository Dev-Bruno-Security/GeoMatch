import React, { useState } from 'react'
import axios from 'axios'

export default function UploadForm({ onResults, apiUrl }) {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  const getApiUrl = () => {
    // Em desenvolvimento, usar URL relativa (proxy)
    // Em produção, usar a URL completa
    return import.meta.env.DEV ? '' : apiUrl
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setMessage(null)
    
    try {
      const form = new FormData()
      form.append('file', file)
      const isSql = file.name.toLowerCase().endsWith('.sql')
      const endpoint = isSql ? '/api/upload/sql' : '/api/upload/csv'
      const baseUrl = getApiUrl()
      const url = `${baseUrl}${endpoint}`
      
      console.log(`Enviando arquivo para: ${url}`)
      console.log(`Environment DEV: ${import.meta.env.DEV}`)
      
      const res = await axios.post(url, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      
      console.log('Upload bem-sucedido:', res.data)
      onResults(res.data)
      setMessage({ type: 'success', text: `Enviado! ${res.data.length} endereco(s) processado(s).` })
      setFile(null)
      e.target.reset()
    } catch (err) {
      console.error('Erro no upload:', err)
      
      let errorMsg = 'Falha no upload.'
      if (err.response?.status === 400) {
        errorMsg = `Erro: ${err.response.data?.detail || 'Arquivo invalido'}`
      } else if (err.response?.status === 0 || !err.response) {
        errorMsg = `Erro de conexao. Certifique-se que o backend esta rodando em http://localhost:8000`
      } else if (err.message === 'Network Error') {
        errorMsg = `Erro de rede. Backend indisponivel em http://localhost:8000`
      } else {
        errorMsg = err.response?.data?.detail || err.message || errorMsg
      }
      
      setMessage({ type: 'error', text: errorMsg })
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <form onSubmit={onSubmit} style={{ 
        marginTop: '1.5rem', 
        padding: '1.5rem',
        background: '#f8f9fa',
        borderRadius: '8px',
        border: '2px dashed #ddd'
      }}>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ 
            display: 'block', 
            marginBottom: '0.5rem', 
            fontWeight: 600,
            color: '#333'
          }}>
            📁 Selecione um arquivo (CSV ou SQL)
          </label>
          <input 
            type="file" 
            accept=".csv,.sql" 
            onChange={(e) => setFile(e.target.files[0])}
            style={{ width: '100%' }}
          />
        </div>
        
        <button 
          type="submit" 
          disabled={loading || !file}
          style={{ 
            width: '100%',
            padding: '0.75rem',
            fontSize: '1rem'
          }}
        >
          {loading ? '⏳ Processando...' : '🚀 Enviar e Processar'}
        </button>
      </form>

      {message && (
        <div className={`status-message status-${message.type}`} style={{ marginTop: '1rem' }}>
          {message.text}
        </div>
      )}
    </>
  )
}
