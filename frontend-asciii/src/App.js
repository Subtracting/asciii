import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [image, setImage] = useState(null);
  const [size, setSize] = useState(6);
  const [fontscale, setFontScale] = useState(16)
  const [mapping, setMapping] = useState(".,;/}%#$")

  const handleFileChange = (event) => {
    setFile(event.target.files[0])
  };

  const handleSizeChange = (event) => {
    setSize(event.target.value)
  };

  const handleScaleChange = (event) => {
    setFontScale(event.target.value)
  };

  const handleMappingChange = (event) => {
    setMapping(event.target.value)
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    formData.append('size', size);
    formData.append('mapping', mapping)
    formData.append('fontscale', fontscale)

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.data.filename) {
        setImage(`http://127.0.0.1:5000/api/output/${response.data.filename}`)
      }
    } catch(error) {
        console.error('There was an error!', error);
      }
  };

  return (
    <div className="App">
      <h1>Asciii Renderer</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Render</button>
      <input type="range" min="1" max="15" defaultValue="6" id="slider" onChange={handleSizeChange}></input>
      <input type="range" min="1" max="32" defaultValue="16" id="slider" onChange={handleScaleChange}></input>
      <input type="input" defaultValue={mapping} onChange={handleMappingChange}></input>
        <div>
          <h3>Rendered Image:</h3>
          {!image ? (
                <img src="https://s4.ezgif.com/tmp/ezgif-4-a301f7ac6f.gif" alt="loading..."  width="250" />
            ) : (
                <img src={image} alt="Uploaded" style={{ maxWidth: '100%' }} />
            )}
        </div>
    </div>
  );
}
export default App;
