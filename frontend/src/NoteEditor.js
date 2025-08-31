import React, { useState, useEffect } from 'react';

function NoteEditor({ selectedNote, onSaveNote, onDeleteNote }) {
  const [content, setContent] = useState('');

  useEffect(() => {
    if (selectedNote) {
      setContent(selectedNote.content);
    } else {
      setContent('');
    }
  }, [selectedNote]);

  const handleSave = () => {
    onSaveNote({ content });
  };

  const handleDelete = () => {
    onDeleteNote(selectedNote.filename);
  };

  return (
    <div className="note-editor">
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <div className="editor-buttons">
        <button onClick={handleSave}>Save</button>
        {selectedNote && <button onClick={handleDelete}>Delete</button>}
      </div>
    </div>
  );
}

export default NoteEditor;
