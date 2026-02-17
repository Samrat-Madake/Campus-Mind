// import { useState } from "react";
// import { submitMentorAnswer } from "../api/client";

// import ConfidenceBadge from "./ConfidenceBadge";

// function MentorTicket({ ticket, onResolved }) {
//   const [answer, setAnswer] = useState("");
//   const [loading, setLoading] = useState(false);

//   const handleSubmit = async () => {
//     if (!answer.trim()) return;

//     setLoading(true);
//     try {
//       await submitMentorAnswer(ticket.id, answer);
//       onResolved(ticket.id);
//     } catch (err) {
//       alert("Failed to submit answer : ", err);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div
//       style={{
//         border: "1px solid #444",
//         padding: "15px",
//         marginBottom: "15px",
//         borderRadius: "4px",
//       }}
//     >
//       <p>
//         <strong>Question:</strong> {ticket.question}
//       </p>

//       <p>
//         <strong>Confidence:</strong>{" "}
//         <ConfidenceBadge confidence={ticket.confidence} />{" "}
//         <span style={{ marginLeft: "8px" }}>({ticket.confidence})</span>
//       </p>
//       <p>
//         <strong>Sources:</strong>
//       </p>
//       <ul>
//         {ticket.sources.map((s, idx) => (
//           <li key={idx}>
//             {s.source} (page {s.page})
//           </li>
//         ))}
//       </ul>

//       <textarea
//         rows={3}
//         style={{ width: "100%", padding: "8px" }}
//         placeholder="Write verified answer..."
//         value={answer}
//         onChange={(e) => setAnswer(e.target.value)}
//       />

//       <button
//         onClick={handleSubmit}
//         disabled={loading}
//         style={{ marginTop: "8px" }}
//       >
//         {loading ? "Submitting..." : "Submit Answer"}
//       </button>
//     </div>
//   );
// }

// export default MentorTicket;

import { useState } from "react";
import { submitMentorAnswer } from "../api/client";
import ConfidenceBadge from "./ConfidenceBadge";

function MentorTicket({ ticket, onResolved }) {
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!answer.trim()) return;

    setLoading(true);
    try {
      await submitMentorAnswer(ticket.id, answer);
      onResolved(ticket.id);
    } catch (err) {
      alert("Failed to submit answer: " + err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ticket-card">
      <div style={{ marginBottom: "15px" }}>
        <h4 style={{ margin: "0 0 8px 0", color: "#4b5563" }}>Student Asked:</h4>
        <p style={{ margin: 0, fontWeight: "500", fontSize: "1.1rem" }}>
          {ticket.question}
        </p>
      </div>

      <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
        <ConfidenceBadge confidence={ticket.confidence} />
        <span style={{ fontSize: "0.85rem", color: "#888", alignSelf: "center" }}>
          Score: {ticket.confidence}
        </span>
      </div>

      {ticket.sources.length > 0 && (
        <div style={{ 
            background: "#f9fafb", 
            padding: "10px", 
            borderRadius: "6px", 
            marginBottom: "15px",
            fontSize: "0.85rem" 
        }}>
          <strong style={{color: "#4b5563"}}>System Sources:</strong>
          <ul style={{ margin: "5px 0 0 20px", padding: 0 }}>
            {ticket.sources.map((s, idx) => (
              <li key={idx} style={{marginBottom: '4px'}}>
                {s.source} (p. {s.page})
              </li>
            ))}
          </ul>
        </div>
      )}

      <div style={{ marginTop: "auto" }}>
        <textarea
          rows={4}
          style={{
            width: "100%",
            padding: "10px",
            border: "1px solid #e5e7eb",
            borderRadius: "8px",
            fontFamily: "inherit",
            marginBottom: "10px",
            resize: "vertical"
          }}
          placeholder="Type your verified answer..."
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
        />
        
        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{
            width: "100%",
            padding: "10px",
            backgroundColor: loading ? "#9ca3af" : "#10b981", // Green for 'Approve/Submit'
            color: "white",
            border: "none",
            borderRadius: "6px",
            fontWeight: "600",
            cursor: loading ? "not-allowed" : "pointer"
          }}
        >
          {loading ? "Submitting..." : "Submit Resolution"}
        </button>
      </div>
    </div>
  );
}

export default MentorTicket;