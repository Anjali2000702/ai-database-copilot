import { useState } from 'react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAskAI = async () => {
    if (!query) return;
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('https://ai-database-copilot-fqmm.onrender.com/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_query: query })
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Backend connection error:", error);
      alert("Error connecting to backend!");
    }
    
    setLoading(false);
  }

  return (
    <div style={{ maxWidth: '900px', margin: '50px auto', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ color: '#2c3e50', textAlign: 'center' }}>🤖 AI Database Copilot</h1>
      <p style={{ textAlign: 'center', color: '#7f8c8d' }}>Ask questions in plain English, get real database insights instantly.</p>

      <div style={{ display: 'flex', gap: '10px', marginTop: '30px' }}>
        <input 
          type="text" 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. What is the total price of orders placed by customer ID 1?" 
          style={{ flex: 1, padding: '15px', fontSize: '16px', borderRadius: '8px', border: '1px solid #ccc' }}
        />
        <button 
          onClick={handleAskAI}
          disabled={loading}
          style={{ padding: '15px 30px', fontSize: '16px', backgroundColor: '#3498db', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
        >
          {loading ? 'Thinking... 🤔' : 'Ask AI ✨'}
        </button>
      </div>

      {result && (
        <div style={{ marginTop: '40px', padding: '25px', backgroundColor: '#f8f9fa', borderRadius: '12px', border: '1px solid #e9ecef' }}>
          
          <h3 style={{ color: '#2c3e50', marginTop: 0 }}>📝 AI Explanation:</h3>
          <p style={{ fontSize: '16px', lineHeight: '1.5', color: '#333' }}>{result.explanation}</p>
          
          {/* 👈 Naya Data Table Section */}
          {result.data && result.data.length > 0 && (
            <div style={{ marginTop: '25px' }}>
              <h3 style={{ color: '#27ae60' }}>📊 Real Database Result:</h3>
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: 'white' }}>
                  <thead>
                    <tr style={{ backgroundColor: '#2c3e50', color: 'white' }}>
                      {Object.keys(result.data[0]).map((key) => (
                        <th key={key} style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'left' }}>{key}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {result.data.map((row, index) => (
                      <tr key={index}>
                        {Object.values(row).map((val, i) => (
                          <td key={i} style={{ padding: '12px', border: '1px solid #ddd' }}>{String(val)}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <h3 style={{ color: '#2c3e50', marginTop: '25px' }}>💻 Generated SQL:</h3>
          <pre style={{ backgroundColor: '#282c34', color: '#61dafb', padding: '15px', borderRadius: '8px', overflowX: 'auto' }}>
            <code>{result.sql_query}</code>
          </pre>

          <p style={{ marginTop: '20px', color: '#e67e22', fontWeight: 'bold' }}>
            ⏱️ Estimated Execution Time: {result.estimated_cost}
          </p>
        </div>
      )}
    </div>
  )
}

export default App