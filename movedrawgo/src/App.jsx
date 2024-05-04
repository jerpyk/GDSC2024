import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import NoteEditor from './NoteEditor';

// App.jsx
function App() {
	return (
	  <main>
		<div className="heading">
		  <h1>Notes App</h1>
		  <button>Create New</button>
		</div>
  
		<div className="note-container">
		  <div className="note-card">
			<h2>Note 1</h2>
			<p>A bit of text from the note</p>
			<button>Delete</button>
		  </div>
		</div>
  
		<h1>Edit Note</h1>
		<div className="editor">{/* Code for Note Editor */}</div>
		<NoteEditor/>
	  </main>
	);
  }
  
  export default App;
