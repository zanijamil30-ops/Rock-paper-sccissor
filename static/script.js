// =============================
// Rock · Paper · Scissors Game
// =============================

document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".choice");
  const resultText = document.getElementById("result-text");
  const computerText = document.getElementById("computer-choice");
  const userText = document.getElementById("user-choice");

  // Handle user click
  buttons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      const user = btn.dataset.choice;
      userText.textContent = `🧑 You chose: ${user}`;
      resultText.textContent = "⏳ Waiting for computer...";

      try {
        // Call Flask API
        const response = await fetch("/api/play", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user }),
        });

        if (!response.ok) {
          const err = await response.json();
          resultText.textContent = "⚠️ Error: " + (err.error || "Unknown error");
          return;
        }

        const data = await response.json();
        computerText.textContent = `💻 Computer chose: ${data.computer}`;

        if (data.result === "tie") {
          resultText.textContent = "🤝 It's a tie!";
          resultText.style.color = "#f39c12";
        } else if (data.result === "user") {
          resultText.textContent = "🎉 You win!";
          resultText.style.color = "#27ae60";
        } else {
          resultText.textContent = "😢 Computer wins!";
          resultText.style.color = "#e74c3c";
        }
      } catch (error) {
        resultText.textContent = "⚠️ Network error. Try again.";
      }
    });
  });
});

