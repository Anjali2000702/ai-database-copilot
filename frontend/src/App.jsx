import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: 'user', text: input }];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('https://ai-database-copilot-fqmm.onrender.com/api/chat', {
        user_query: input
      });
      
      setMessages([
        ...newMessages, 
        { 
          sender: 'ai', 
          text: response.data.explanation,
          data: response.data.data,
          sql: response.data.sql_query,         // 👈 Naya: SQL Query capture ki
          cost: response.data.estimated_cost    // 👈 Naya: Cost capture ki
        }
      ]);
    } catch (error) {
      console.error(error);
      setMessages([...newMessages, { sender: 'ai', text: "Error: Backend se connect nahi ho pa raha." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const renderTable = (data) => {
    if (!data || data.length === 0) return null;
    const headers = Object.keys(data[0]);

    return (
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              {headers.map((header, index) => (
                <th key={index}>{header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {headers.map((header, colIndex) => (
                  <td key={colIndex}>{row[header]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="chat-container">
      <h1>AI Data Copilot</h1>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={msg.sender}>
            {/* User ya AI ka main text */}
            <p>{msg.text}</p>
            
            {/* 🧠 AI Agents ki Technical Details */}
            {msg.sender === 'ai' && msg.sql && (
              <div className="tech-details">
                <p className="tech-title">🧠 NL2SQL Agent Generated:</p>
                <pre className="sql-code">{msg.sql}</pre>
                {msg.cost && <span className="cost-badge">💰 Cost Predictor: {msg.cost}</span>}
              </div>
            )}

            {/* Database ka Table */}
            {msg.data && renderTable(msg.data)}
          </div>
        ))}
        {isLoading && <div className="ai"><p>AI is thinking...</p></div>}
      </div>
      <div className="input-area">
        <input 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          placeholder="Database se kuch puchein... (e.g., Show me 5 customers)" 
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          disabled={isLoading}
        />
        <button onClick={sendMessage} disabled={isLoading}>Send</button>
      </div>
    </div>
  );
}

export default App;