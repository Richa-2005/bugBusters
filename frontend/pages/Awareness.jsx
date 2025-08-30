import React from 'react';
import './Awareness.css'; 

const Awareness = () => {
  return (
    <div className="coastal-awareness-container">
      <header className="awareness-header">
        <h1>Coastal Alert Awareness </h1>
        <p>Your guide to staying safe during coastal emergencies.</p>
      </header>

      <section className="info-section grid-layout">
        <div className="info-card">
          <h2>Understanding Alerts</h2>
          <p>
            Coastal alerts can range from advisories to warnings. Know the difference:
            <strong>Advisory</strong> (potential hazard), <strong>Watch</strong> (conditions favorable for hazard),
            <strong>Warning</strong> (hazard imminent or occurring). Always follow local authorities.
          </p>
          <img src="https://www.shutterstock.com/image-vector/tsunami-hazard-zone-warning-sign-600nw-2517327097.jpg" alt="Coastal Alert Warning Sign" className="card-image" />
        </div>

        <div className="info-card">
          <h2>Emergency Kit Essentials</h2>
          <p>
            A well-packed kit can make all the difference. Include water, non-perishable food,
            first-aid, flashlight, radio, extra batteries, whistle, and personal documents.
          </p>
          <img src="https://images-na.ssl-images-amazon.com/images/I/81k6JStLeqL._AC_UL495_SR435,495_.jpg" alt="Emergency kit contents" className="card-image" />
        </div>
<br />
        <div className="info-card">
          <h2>Secure Your Home</h2>
          <p>
            Before an alert becomes a warning, secure loose outdoor items, clear drains,
            and consider sandbags if in a flood-prone area. Unplug non-essential electronics.
          </p>
          <img src="https://content.presspage.com/uploads/1441/1920_tsunami-2.jpg?10000" alt="Securing a coastal home" className="card-image" />
        </div>

        <div className="info-card">
          <h2>Evacuation Routes</h2>
          <p>
            Familiarize yourself with local evacuation routes. Always follow official evacuation orders
            and head to designated safe zones or shelters. Don't wait until it's too late.
          </p>
          <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFAbM26KtR6lfMl8PMlmtTXO6fbIzU9e1XKgMOxk5GEOEATIWeCKJu_jsbSkkjE6RIfoQ&usqp=CAU" alt="Coastal evacuation routes" className="card-image" />
        </div>
      </section>

      <section className="video-section">
        <h2>Watch & Learn: Official Guidance</h2>
        <p>These videos from trusted sources provide vital information for coastal safety.</p>

        <div className="video-grid">
          <div className="video-card">
            <h3>Red Cross: Flood Safety</h3>
            <div className="video-responsive">
              <iframe
                src="https://www.youtube.com/embed/Glc-1f4Ez00"
                title="Red Cross Flood Preparedness"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            </div>
            <p>Essential steps to prepare for and respond to floods. (Source: American Red Cross)</p>
          </div>


          <div className="video-card">
            <h3>Red Cross: Disaster Preparedness</h3>
            <div className="video-responsive">
              <iframe
                src="https://www.youtube.com/embed/mLPYViT2k-U"
                title="Disaster Preparedness"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            </div>
            <p>A video on general disaster preparedness, relevant for coastal residents. (Source: American Red Cross)</p>
          </div>
        </div>
      </section>

      <section className="call-to-action">
        <h2>Stay Informed, Stay Safe!</h2>
        <p>
          Always monitor local news, weather alerts, and official government channels for the latest information.
          Your preparedness saves lives!
        </p>
        <a href="https://www.ready.gov/alerts" target="_blank" rel="noopener noreferrer" className="cta-button">
          Find More Info at Ready.gov
        </a>
      </section>

      <footer className="awareness-footer">
        <p>&copy; 2023 Coastal Safety Initiative. Information for public awareness only.</p>
      </footer>
    </div>
  );
};

export default Awareness;