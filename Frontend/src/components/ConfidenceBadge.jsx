// function ConfidenceBadge({ confidence }) {
//   let color = "#999";
//   let label = "Unknown";

//   if (confidence >= 0.7) {
//     color = "green";
//     label = "High confidence";
//   } else if (confidence >= 0.4) {
//     color = "orange";
//     label = "Medium confidence";
//   } else {
//     color = "red";
//     label = "Low confidence";
//   }

//   return (
//     <span
//       style={{
//         display: "inline-block",
//         padding: "4px 10px",
//         borderRadius: "12px",
//         backgroundColor: color,
//         color: "white",
//         fontSize: "12px",
//         fontWeight: "bold",
//       }}
//     >
//       {label}
//     </span>
//   );
// }

// export default ConfidenceBadge;
function ConfidenceBadge({ confidence }) {
    let bgColor = "#e5e7eb";
    let textColor = "#374151";
    let label = "Unknown";
  
    if (confidence >= 0.7) {
      bgColor = "#d1fae5"; // Light Green
      textColor = "#065f46"; // Dark Green
      label = "High Confidence";
    } else if (confidence >= 0.4) {
      bgColor = "#fef3c7"; // Light Orange
      textColor = "#92400e"; // Dark Orange
      label = "Medium Confidence";
    } else {
      bgColor = "#fee2e2"; // Light Red
      textColor = "#991b1b"; // Dark Red
      label = "Low Confidence";
    }
  
    return (
      <span
        style={{
          display: "inline-flex",
          padding: "4px 12px",
          borderRadius: "9999px",
          backgroundColor: bgColor,
          color: textColor,
          fontSize: "0.75rem",
          fontWeight: "700",
          letterSpacing: "0.025em"
        }}
      >
        {label}
      </span>
    );
  }
  
  export default ConfidenceBadge;