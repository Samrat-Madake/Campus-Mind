import { useState } from "react";
import StudentChat from "./pages/StudentChat";
import MentorPanel from "./pages/MentorPanel";
import VerifiedAnswers from "./pages/VerifiedAnswers";
import "./App.css";

function App() {
  const [role, setRole] = useState("student");

  const getHeaderTitle = () => {
    if (role === "student") return "Ask a Question";
    if (role === "mentor") return "Mentor Dashboard";
    if (role === "verified") return "Faculty Verified Answers";
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="brand">
          <span style={{ fontSize: "24px" }}>🎓</span> CampusMind
        </div>

        <nav>
          <button
            className={`nav-btn ${role === "student" ? "active" : ""}`}
            onClick={() => setRole("student")}
          >
            <span>💬</span> Student Chat
          </button>

          <button
            className={`nav-btn ${role === "mentor" ? "active" : ""}`}
            onClick={() => setRole("mentor")}
          >
            <span>🛡️</span> Mentor Panel
          </button>

          <button
            className={`nav-btn ${role === "verified" ? "active" : ""}`}
            onClick={() => setRole("verified")}
          >
            <span>📘</span> Verified Answers
          </button>
        </nav>
      </aside>

      <main className="main-content">
        <header className="header">{getHeaderTitle()}</header>

        {role === "student" && <StudentChat />}
        {role === "mentor" && <MentorPanel />}
        {role === "verified" && <VerifiedAnswers />}
      </main>
    </div>
  );
}

export default App;
