import React from 'react';

// Profile Card Component - Day 22 Project

// Main ProfileCard Component
function ProfileCard() {
  const profiles = [
    {
      id: 1,
      name: "John Doe",
      title: "Frontend Developer",
      bio: "Passionate about creating beautiful UIs",
      image: "https://via.placeholder.com/150",
      skills: ["React", "JavaScript", "CSS"]
    },
    {
      id: 2,
      name: "Jane Smith",
      title: "UI/UX Designer",
      bio: "Creative designer with eye for detail",
      image: "https://via.placeholder.com/150",
      skills: ["Figma", "Adobe XD", "UI Design"]
    },
    {
      id: 3,
      name: "Bob Johnson",
      title: "Full Stack Developer",
      bio: "Building complete web applications",
      image: "https://via.placeholder.com/150",
      skills: ["Node.js", "React", "MongoDB"]
    }
  ];

  return (
    <div className="profile-container">
      <h1>Meet Our Team</h1>
      <div className="profiles-grid">
        {profiles.map(profile => (
          <Card key={profile.id} profile={profile} />
        ))}
      </div>
    </div>
  );
}

// Reusable Card Component
function Card({ profile }) {
  return (
    <div className="card">
      <img src={profile.image} alt={profile.name} className="card-image" />
      <div className="card-content">
        <h2>{profile.name}</h2>
        <p className="title">{profile.title}</p>
        <p className="bio">{profile.bio}</p>
        
        <div className="skills">
          <h4>Skills:</h4>
          <ul>
            {profile.skills.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
        </div>

        <button className="btn">View Profile</button>
      </div>
    </div>
  );
}

// Greeting Component - Simple Component Example
function Greeting({ name = "Guest", time = "morning" }) {
  const greetings = {
    morning: "Good morning",
    afternoon: "Good afternoon",
    evening: "Good evening"
  };

  return (
    <div className="greeting">
      <h2>{greetings[time]}, {name}!</h2>
      <p>Welcome to React learning</p>
    </div>
  );
}

// Header Component
function Header() {
  return (
    <header className="header">
      <div className="logo">My React App</div>
      <nav className="nav">
        <a href="#home">Home</a>
        <a href="#about">About</a>
        <a href="#contact">Contact</a>
      </nav>
    </header>
  );
}

// Footer Component
function Footer() {
  return (
    <footer className="footer">
      <p>&copy; 2024 React Learning Journey</p>
    </footer>
  );
}

// Main App Component
export default function App() {
  return (
    <>
      <Header />
      <Greeting name="Student" time="morning" />
      <main className="main-content">
        <ProfileCard />
      </main>
      <Footer />
    </>
  );
}

/* CSS Styles (Save as App.css or in a CSS module) */
export const styles = `
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
}

.logo {
  font-size: 24px;
  font-weight: bold;
}

.nav {
  display: flex;
  gap: 30px;
}

.nav a {
  color: white;
  text-decoration: none;
  transition: color 0.3s;
}

.nav a:hover {
  color: #ffdd00;
}

.greeting {
  background: white;
  padding: 30px;
  text-align: center;
  margin: 20px;
  border-radius: 8px;
}

.main-content {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 20px;
}

.profile-container {
  text-align: center;
}

.profile-container h1 {
  margin-bottom: 40px;
  color: #333;
}

.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-content {
  padding: 20px;
}

.card-content h2 {
  color: #333;
  margin-bottom: 8px;
}

.title {
  color: #667eea;
  font-weight: bold;
  margin-bottom: 10px;
}

.bio {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.6;
}

.skills {
  text-align: left;
  margin-bottom: 15px;
}

.skills h4 {
  color: #333;
  margin-bottom: 8px;
}

.skills ul {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skills li {
  background: #e3f2fd;
  color: #0066cc;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
}

.btn {
  width: 100%;
  padding: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: opacity 0.3s;
}

.btn:hover {
  opacity: 0.8;
}

.footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 20px;
  margin-top: 40px;
}
`;
