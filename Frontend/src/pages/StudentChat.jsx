

import { useState, useRef, useEffect } from "react";
import { askQuestion } from "../api/client";
import ReactMarkdown from "react-markdown";
import ConfidenceBadge from "../components/ConfidenceBadge";

const STORAGE_KEY = "campus_mind_chat_history";

function StudentChat() {
  const [question, setQuestion] = useState("");

  // ✅ Load history from localStorage ONCE
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Auto-scroll to bottom
  const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // ✅ Persist messages on every change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
  }, [messages]);

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userMsg = { role: "user", content: question };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setError(null);
    setQuestion("");

    try {
      const res = await askQuestion(userMsg.content);

      const botMsg = {
        role: "bot",
        content: res.answer,
        confidence: res.confidence,
        action: res.action,
        sources: res.sources,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setError("Something went wrong. Please try again. Error :",err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  return (
    <>
      <div className="chat-container">
        {messages.length === 0 && !loading && (
          <div style={{ textAlign: "center", marginTop: "100px", color: "#6b7280" }}>
            <div style={{ fontSize: "40px", marginBottom: "20px" }}>👋</div>
            <h3>Welcome to Campus Mind</h3>
            <p>Ask any question from your syllabus to get started.</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className="message-wrapper">
            <div
              className={`chat-bubble ${
                msg.role === "user" ? "user-msg" : "bot-msg"
              }`}
            >
              {msg.role === "bot" ? (
                <div className="markdown-content">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              ) : (
                msg.content
              )}

              {msg.role === "bot" && (
                <div className="msg-meta">
                  <div
                    style={{ display: "flex", alignItems: "center", gap: "10px" }}
                  >
                    <span style={{ color: "#0b0b0b", fontSize: "0.8rem" }}>
                      Confidence Score {msg.confidence*100}:
                    </span>
                    <ConfidenceBadge confidence={msg.confidence} />
                    {/* <p>Score : {msg.confidence * 100}</p> */}
                  </div>

                  {msg.sources && msg.sources.length > 0 && (
                    <div
                      style={{
                        marginTop: "8px",
                        fontSize: "0.8rem",
                        color: "#666",
                      }}
                    >
                      <strong>Sources:</strong>{" "}
                      {msg.sources.map((s) => s.source).join(", ")}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message-wrapper">
            <div className="chat-bubble bot-msg">
              <span className="loading-dots">Thinking...</span>
            </div>
          </div>
        )}

        {error && (
          <p style={{ color: "red", textAlign: "center" }}>{error}</p>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <textarea
          rows={1}
          className="chat-input"
          placeholder="Type your question here..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          className="send-btn"
          onClick={handleAsk}
          disabled={loading || !question.trim()}
        >
          Send
        </button>
      </div>
    </>
  );
}

export default StudentChat;
