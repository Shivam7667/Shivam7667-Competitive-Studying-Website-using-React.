import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './StudySessionsPage.css';  // Import the CSS file

const StudySessionsPage = () => {
  const [materials, setMaterials] = useState([]);

  const fetchMaterials = async () => {
    try {
      const response = await axios.get('http://localhost:5000/study/materials');
      setMaterials(response.data);
    } catch (error) {
      console.error('Error fetching study materials:', error);
    }
  };

  useEffect(() => {
    fetchMaterials();
  }, []);

  return (
    <div className="study-container">
      <h1 className="study-title">Study Materials</h1>
      <ul className="study-materials-list">
        {materials.map((material, index) => (
          <li key={index} className="study-material-item">
            <img src={material.image} alt={material.title} className="material-image" />
            <div className="material-info">
              <a href={material.url} className="material-title">{material.title}</a>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StudySessionsPage;
