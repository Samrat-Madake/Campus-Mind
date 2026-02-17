import { useEffect, useState } from "react";
import { getVerifiedAnswers } from "../api/client";
import ReactMarkdown from "react-markdown";

function VerifiedAnswers() {
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnswers = async () => {
      try {
        const data = await getVerifiedAnswers();
        setAnswers(data);
      } catch (err) {
        setError("Failed to load verified answers.Error : ", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnswers();
  }, []);

  return (
    <div
      style={{
        flex: 1,
        overflowY: "auto",
        padding: "30px",
        maxWidth: "900px",
        margin: "0 auto",
      }}
    >
      {loading && (
        <div style={{ textAlign: "center", color: "#6b7280" }}>
          Loading verified answers...
        </div>
      )}

      {error && (
        <div style={{ textAlign: "center", color: "red" }}>
          {error}
        </div>
      )}

      {!loading && answers.length === 0 && (
        <div style={{ textAlign: "center", color: "#6b7280" }}>
          <div style={{ fontSize: "40px", marginBottom: "10px" }}>📭</div>
          <h3>No Verified Answers Yet</h3>
          <p>Faculty-reviewed answers will appear here.</p>
        </div>
      )}

      {answers.map((item, idx) => (
        <div
          key={idx}
          className="ticket-card"
          style={{ marginBottom: "20px" }}
        >
          <div style={{ marginBottom: "10px" }}>
            <span className="badge" style={{ background: "#16a34a", color: "white" }}>
              Faculty Verified
            </span>
          </div>

          <h4 style={{ marginBottom: "8px" }}>Question</h4>
          <p style={{ marginBottom: "15px" }}>{item.question}</p>

          <h4 style={{ marginBottom: "8px" }}>Answer</h4>
          <div className="markdown-content">
            <ReactMarkdown>{item.answer}</ReactMarkdown>
          </div>

          {item.sources && item.sources.length > 0 && (
            <div className="meta-info">
              <strong>Sources:</strong>{" "}
              {item.sources.map((s) => s.source).join(", ")}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default VerifiedAnswers;
