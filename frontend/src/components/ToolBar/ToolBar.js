import React, { useState } from 'react';

function Toolbar() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch('http://localhost:8000/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email }),
      });

      const data = await res.json();
      setResponse(data.message);
    } catch (error) {
      console.error('Error:', error);
      setResponse('Failed to connect to the server');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Chess.com UserName:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {response && <p>{response}</p>}
    </div>
  );
}

export default Toolbar;
