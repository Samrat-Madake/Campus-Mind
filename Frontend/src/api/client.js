const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Student asks a question
 */
export async function askQuestion(question) {
  const response = await fetch(`${API_BASE_URL}/query/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error("Failed to get response from server");
  }

  return await response.json();
}

/**
 * Mentor fetches pending questions
 */
export async function getPendingTickets() {
  const response = await fetch(`${API_BASE_URL}/mentor/pending`);

  if (!response.ok) {
    throw new Error("Failed to fetch pending tickets");
  }

  return await response.json();
}

/**
 * Mentor submits an answer
 */
export async function submitMentorAnswer(ticketId, answer) {
  const response = await fetch(
    `${API_BASE_URL}/mentor/answer/${ticketId}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ answer }),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to submit mentor answer");
  }

  return await response.json();
}


export async function getVerifiedAnswers() {
  const res = await fetch("http://localhost:8000/mentor/answered");
  if (!res.ok) {
    throw new Error("Failed to fetch verified answers");
  }
  return res.json();
}
