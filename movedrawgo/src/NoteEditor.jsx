// NoteEditor.jsx
export default function NoteEditor() {
	return (
	  <>
		<input type="text" />
  
		<textarea cols="30" rows="10" />
	  </>
	);
  }
  // NoteEditor.jsx

export default function NoteEditor() {
  const [note, setNote] = useState({ name: "", content: "" });

  return (
    <>
      <input
        type="text"
        value={note.name}
        onChange={(e) => {
          const newNote = { ...note, name: e.target.value };
        }}
      />

      <textarea
        cols="30"
        rows="10"
        value={note.content}
        onChange={(e) => {
          const newNote = { ...note, content: e.target.value };
        }}
      />
    </>
  );
}