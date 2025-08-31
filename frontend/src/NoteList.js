import React from 'react';

function NoteList({ notes, onNoteSelect }) {
  return (
    <div className="note-list">
      <h2>Notes</h2>
      <ul>
        {notes.map(note => (
          <li key={note} onClick={() => onNoteSelect(note)}>
            {note}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default NoteList;
