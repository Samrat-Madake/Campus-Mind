import { useEffect, useState } from "react";
import { getPendingTickets } from "../api/client";
import MentorTicket from "../components/MentorTicket";

function MentorPanel() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchTickets = async () => {
    setLoading(true);
    try {
      const data = await getPendingTickets();
      setTickets(data);
    } catch (err) {
      console.error("Failed to load mentor queue:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  const handleResolved = (ticketId) => {
    setTickets((prev) => prev.filter((t) => t.id !== ticketId));
  };

  return (
    <div style={{ height: '100%', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
      
      {loading && (
        <div style={{ padding: "40px", textAlign: "center", color: "#666" }}>
          Loading pending tickets...
        </div>
      )}

      {!loading && tickets.length === 0 && (
        <div style={{ padding: "40px", textAlign: "center", color: "#666" }}>
          <div style={{ fontSize: "40px", marginBottom: "10px" }}>🎉</div>
          <h3>All caught up!</h3>
          <p>No pending questions for review.</p>
        </div>
      )}

      <div className="mentor-grid">
        {tickets.map((ticket) => (
          <MentorTicket
            key={ticket.id}
            ticket={ticket}
            onResolved={handleResolved}
          />
        ))}
      </div>
    </div>
  );
}

export default MentorPanel;