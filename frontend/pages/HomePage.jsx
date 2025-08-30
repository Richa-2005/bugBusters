import React, { useState } from 'react'
import './homePage.css' 


const SunIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <circle cx="12" cy="12" r="4"></circle>
    <path d="M12 2v2"></path>
    <path d="M12 20v2"></path>
    <path d="m4.93 4.93 1.41 1.41"></path>
    <path d="m17.66 17.66 1.41 1.41"></path>
    <path d="M2 12h2"></path>
    <path d="M20 12h2"></path>
    <path d="m6.34 17.66-1.41 1.41"></path>
    <path d="m19.07 4.93-1.41 1.41"></path>
  </svg>
)
const SunsetIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M12 10V2"></path>
    <path d="m4.93 10.93 1.41 1.41"></path>
    <path d="M2 18h2"></path>
    <path d="M20 18h2"></path>
    <path d="m19.07 12.34-1.41-1.41"></path>
    <path d="M22 22H2"></path>
    <path d="m16 6-4 4-4-4"></path>
    <path d="M12 10v8"></path>
  </svg>
)
const ThermometerIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"></path>
  </svg>
)
const DropletIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"></path>
  </svg>
)
const EyeIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
    <circle cx="12" cy="12" r="3"></circle>
  </svg>
)
const WindIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"></path>
    <path d="M9.6 4.6A2 2 0 1 1 11 8H2"></path>
    <path d="M12.6 19.4A2 2 0 1 0 14 16H2"></path>
  </svg>
)
const GaugeIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="m12 14 4-4"></path>
    <path d="M3.34 19a10 10 0 1 1 17.32 0"></path>
  </svg>
)
const CloudIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"></path>
  </svg>
)
const CompassIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <circle cx="12" cy="12" r="10"></circle>
    <polygon points="16.24 7.76 -7.76 16.24 12 12 7.76 16.24 16.24 7.76"></polygon>
  </svg>
)

// --- Main HomePage Component ---
const HomePage = ({ userCity = 'Ahmedabad' }) => {
  // State to hold all weather data.
  const [weatherData, setWeatherData] = useState({
    temperature: 29,
    feelsLike: 32,
    humidity: 78,
    windSpeed: 15,
    visibility: '10km',
    pressure: 1012,
    sunrise: '6:15 AM',
    sunset: '7:05 PM',
    clouds: 40,
    windDegree: 210,
  })

  // An array to easily map over and render the detail cards
  const weatherDetails = [
    { title: 'Sunrise', value: weatherData.sunrise, icon: <SunIcon /> },
    { title: 'Sunset', value: weatherData.sunset, icon: <SunsetIcon /> },
    {
      title: 'Humidity',
      value: `${weatherData.humidity}%`,
      icon: <DropletIcon />,
    },
    { title: 'Visibility', value: weatherData.visibility, icon: <EyeIcon /> },
    {
      title: 'Feels Like',
      value: `${weatherData.feelsLike}°C`,
      icon: <ThermometerIcon />,
    },
    {
      title: 'Wind Degree',
      value: `${weatherData.windDegree}°`,
      icon: <CompassIcon />,
    },
    {
      title: 'Wind Speed',
      value: `${weatherData.windSpeed} km/h`,
      icon: <WindIcon />,
    },
    { title: 'Clouds', value: `${weatherData.clouds}%`, icon: <CloudIcon /> },
    {
      title: 'Pressure',
      value: `${weatherData.pressure} hPa`,
      icon: <GaugeIcon />,
    },
  ]

  return (
    <div className="weather-app-container">
      <main className="weather-card">
        {/* --- Top Section: City and Temperature --- */}
        <div className="main-info">
          <h1 className="city-name">{userCity}</h1>
          <p className="temperature">
            {weatherData.temperature}°<span className="degree-symbol">C</span>
          </p>
          <p className="weather-description">Mostly Cloudy</p>
        </div>

        {/* --- Bottom Section: Weather Details Grid --- */}
        <div className="highlights-section">
          <h2 className="highlights-title">Today's Highlights</h2>
          <div className="details-grid">
            {weatherDetails.map((detail, index) => (
              <div key={index} className="detail-card">
                <div className="detail-card-header">
                  <span className="detail-title">{detail.title}</span>
                  {detail.icon}
                </div>
                <p className="detail-value">{detail.value}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
      <footer className="app-footer">
        <p>Weather data is for demonstration purposes.</p>
      </footer>
    </div>
  )
}

export default HomePage