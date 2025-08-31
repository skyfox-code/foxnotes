import React, { useState, useEffect } from 'react';
import NoteList from './NoteList';
import NoteEditor from './NoteEditor';
import './App.css';

function App() {
  const [notes, setNotes] = useState([]);
  const [selectedNote, setSelectedNote] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/notes')
      .then(res => res.json())
      .then(data => setNotes(data));
  }, []);

  const handleNoteSelect = (note) => {
    fetch(`http://localhost:5000/api/notes/${note}`)
      .then(res => res.json())
      .then(data => setSelectedNote({ filename: note, content: data.content }));
  };

  const handleSaveNote = (note) => {
    fetch('http://localhost:5000/api/notes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(note),
    })
      .then(res => res.json())
      .then(data => {
        setNotes([...notes, data.filename]);
        setSelectedNote({ filename: data.filename, content: note.content });
      });
  };

  const handleDeleteNote = (filename) => {
    fetch(`http://localhost:5000/api/notes/${filename}`, {
      method: 'DELETE',
    })
      .then(() => {
        setNotes(notes.filter(note => note !== filename));
        setSelectedNote(null);
      });
  };

  return (
    <div className="App">
      <div className="sidebar">
        <NoteList notes={notes} onNoteSelect={handleNoteSelect} />
      </div>
      <div className="main-content">
        <NoteEditor selectedNote={selectedNote} onSaveNote={handleSaveNote} onDeleteNote={handleDeleteNote} />
      </div>
    </div>
  );
}

export default App;