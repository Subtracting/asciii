import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

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
      <div className='header'>
        <h1>Asciii Renderer</h1>
      </div>
      <div className='main'>

        <div className='image-container'>
            {!image ? (
                  <div>Loading...</div>
              ) : (
                  <img src={image} alt="Uploaded" style={{ maxWidth: '100%' }} />
              )}
          </div>

        <div className='controls-container'>
          <label for="files" className="upload-btn">Select Image</label>
          <div className='selected-file'>{
            file ? `${file.name}` : "No file selected..."}
          </div>
          <input hidden type="file" id="files" className="file-input" onChange={handleFileChange}/>
          size
          <input type="range" min="1" max="15" defaultValue="6" id="size" className='slider-input' onChange={handleSizeChange}></input>
          scale
          <input type="range" min="1" max="32" defaultValue="16" id="scale" className='slider-input' onChange={handleScaleChange}></input>
          mapping
          <input type="input" defaultValue={mapping} className="mapping-input" onChange={handleMappingChange}></input>
          <button className="render-button" onClick={handleUpload}>Render</button>
        </div>

        </div>
    </div>
  );
}
export default App;
