import React from 'react'

function getClassificationBadge(classification) {
  const badges = {
    'MATCH_CONFIRMADO': { class: 'badge-success', text: '🟢 Confirmado' },
    'MATCH_PROVAVEL': { class: 'badge-warning', text: '🟡 Provável' },
    'MATCH_POSSIVEL': { class: 'badge-info', text: '🟠 Possível' },
    'MATCH_INDEFINIDO': { class: 'badge-info', text: '🔵 Indefinido' },
    'NO_MATCH': { class: 'badge-danger', text: '🔴 Sem Match' }
  }
  const badge = badges[classification] || { class: 'badge-info', text: classification }
  return <span className={`badge ${badge.class}`}>{badge.text}</span>
}

export default function ResultsTable({ rows }) {
  if (!rows || rows.length === 0) {
    return (
      <div style={{ 
        padding: '2rem', 
        textAlign: 'center', 
        color: '#666',
        background: '#f8f9fa',
        borderRadius: '8px'
      }}>
        📭 Nenhum resultado ainda. Faça upload de um arquivo para começar!
      </div>
    )
  }

  return (
    <div style={{ overflowX: 'auto', marginTop: '1.5rem' }}>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Endereço Original</th>
            <th>CEP</th>
            <th>Normalizado</th>
            <th>Provedor</th>
            <th>Endereço Validado</th>
            <th>CEP Validado</th>
            <th>Score</th>
            <th>Classificação</th>
            <th>Vencedor</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            r.results.map((pr, idx) => {
              const isWinner = r.winner_provider && pr.provider_name === r.winner_provider
              const cepMatch = r.cep && pr.cep && r.cep === pr.cep
              return (
                <tr key={`${r.id}-${idx}`} style={isWinner ? { background: '#f0f9ff' } : {}}>
                  <td style={{ fontWeight: 'bold', color: '#667eea' }}>#{r.id}</td>
                  <td style={{ maxWidth: '200px', wordWrap: 'break-word' }}>
                    {r.raw_address}
                  </td>
                  <td style={{ 
                    fontFamily: 'monospace',
                    fontSize: '0.9em',
                    fontWeight: r.cep ? '600' : 'normal',
                    color: r.cep ? '#059669' : '#9ca3af'
                  }}>
                    {r.cep ? `${r.cep.slice(0,5)}-${r.cep.slice(5)}` : '-'}
                  </td>
                  <td style={{ fontSize: '0.9em', color: '#666' }}>
                    {r.normalized_address}
                  </td>
                  <td>
                    <span style={{ 
                      padding: '0.25rem 0.5rem',
                      background: '#e0e7ff',
                      borderRadius: '4px',
                      fontSize: '0.85rem',
                      fontWeight: '500'
                    }}>
                      {pr.provider_name}
                    </span>
                  </td>
                  <td style={{ maxWidth: '250px', wordWrap: 'break-word' }}>
                    {pr.matched_address || '-'}
                  </td>
                  <td style={{ 
                    fontFamily: 'monospace',
                    fontSize: '0.9em',
                    fontWeight: pr.cep ? '600' : 'normal',
                    color: cepMatch ? '#059669' : (pr.cep ? '#f59e0b' : '#9ca3af'),
                    background: cepMatch ? '#d1fae5' : 'transparent',
                    padding: '0.5rem'
                  }}>
                    {pr.cep ? `${pr.cep.slice(0,5)}-${pr.cep.slice(5)}` : '-'}
                    {cepMatch && ' ✓'}
                  </td>
                  <td style={{ 
                    fontWeight: 'bold',
                    fontSize: '1.1rem',
                    color: pr.score >= 90 ? '#22c55e' : pr.score >= 70 ? '#eab308' : '#64748b'
                  }}>
                    {pr.score ? `${pr.score.toFixed(1)}%` : '-'}
                  </td>
                  <td>
                    {pr.classification ? getClassificationBadge(pr.classification) : '-'}
                  </td>
                  <td style={{ textAlign: 'center', fontSize: '1.5rem' }}>
                    {isWinner ? '🏆' : ''}
                  </td>
                </tr>
              )
            })
          ))}
        </tbody>
      </table>
      
      <div style={{ 
        marginTop: '1rem', 
        padding: '1rem',
        background: '#f8f9fa',
        borderRadius: '6px',
        fontSize: '0.9rem',
        color: '#666'
      }}>
        💡 <strong>Total:</strong> {rows.length} endereços processados | 
        <strong> Provedores:</strong> {rows[0]?.results?.length || 0} por endereço |
        <strong> CEPs encontrados:</strong> {rows.filter(r => r.cep).length}
      </div>
    </div>
  )
}
