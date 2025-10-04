// Get elements
const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const chatbox = document.getElementById("chatbox");
const micBtn = document.getElementById("micBtn"); // optional for future voice input

// Function to append messages
function appendMessage(message, sender) {
  const msgDiv = document.createElement("p");
  msgDiv.textContent = message;
  msgDiv.classList.add(sender === "user" ? "user-msg" : "bot-msg");
  chatbox.appendChild(msgDiv);
  chatbox.scrollTop = chatbox.scrollHeight; // auto scroll
}

// Function to send user message
async function sendMessage() {
  let message = userInput.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  userInput.value = "";

  try {
    const response = await fetch("/predict_crimes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_input: message }),
    });

    const data = await response.json();
    let botMsg = "";

    if (data.predicted_crimes !== undefined) {
      botMsg = `Predicted Total Crimes: ${data.predicted_crimes}`;
      if (data.tip) botMsg += `. Safety Tip: ${data.tip}`;
      if (data.helplines) {
        botMsg += `. Helplines: Police ${data.helplines.Police}, Women Helpline ${data.helplines["Women Helpline"]}`;
      }
    } else if (data.response) {
      botMsg = data.response;
    } else if (data.error) {
      botMsg = `Error: ${data.error}`;
    } else {
      botMsg = "Sorry, could not process your request.";
    }

    appendMessage(botMsg, "bot");
    window.speechSynthesis.speak(new SpeechSynthesisUtterance(botMsg));
  } catch (error) {
    console.error(error);
    const errMsg = "Sorry, something went wrong. Try again.";
    appendMessage(errMsg, "bot");
    window.speechSynthesis.speak(new SpeechSynthesisUtterance(errMsg));
  }
}

// Send message on button click
sendBtn.addEventListener("click", sendMessage);

// Optional: send message on Enter key
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});

// Voice input using Web Speech API
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;

  micBtn.addEventListener("click", () => {
    recognition.start();
  });

  recognition.addEventListener("result", (e) => {
    const transcript = e.results[0][0].transcript;
    userInput.value = transcript;
    sendMessage(); // optionally send automatically
  });

  recognition.addEventListener("error", (e) => {
    console.error("Speech recognition error:", e.error);
    alert("Voice input failed. Try again.");
  });
} else {
  micBtn.addEventListener("click", () => {
    alert("Your browser does not support speech recognition.");
  });
}

// -------------------- Carousel Rotation --------------------
document.addEventListener("DOMContentLoaded", function () {
  const images = document.querySelectorAll(".left-panel .carousel img");
  let current = 0;

  function rotateImages() {
    images[current].classList.remove("active");
    current = (current + 1) % images.length;
    images[current].classList.add("active");
  }

  setInterval(rotateImages, 3000); // rotate every 3 seconds
});
