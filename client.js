import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [text, setText] = useState("");
  const [imageURL, setImageURL] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await axios.post("/practice", {
      text: text,
    });
    console.log(response.data);
  };

  const handleRender = async (event) => {
    event.preventDefault();
    const response = await axios.post("/render", {
      input_file: "input.txt",
    });
    setImageURL(response.data.image_url);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="text" value={text} onChange={(event) => setText(event.target.value)} />
        <button type="submit">Generate Dataset</button>
      </form>
      <button onClick={handleRender}>Render Handwriting</button>
      {imageURL && <img src={imageURL} alt="Handwriting Image" />}
    </div>
  );
}

export default App;