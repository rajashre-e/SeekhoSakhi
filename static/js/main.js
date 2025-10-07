// -------------------- Get elements --------------------
const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const chatbox = document.getElementById("chatbox");
const micBtn = document.getElementById("micBtn");

// -------------------- Append messages to chatbox --------------------
function appendMessage(message, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message-bubble", sender === "user" ? "user-msg" : "bot-msg");

    // Markdown-like formatting
    const formatted = message
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.*?)\*/g, "<em>$1</em>");

    const textSpan = document.createElement("span");
    textSpan.innerHTML = formatted;
    msgDiv.appendChild(textSpan);

    // Add speaker button only for bot messages
    if (sender === "bot") {
        const speakerBtn = document.createElement("button");
        speakerBtn.textContent = "🔊";
        speakerBtn.classList.add("speaker-btn");
        let audio = null;
        let playing = false;

        speakerBtn.addEventListener("click", async () => {
            if (!audio) {
                try {
                    const response = await fetch("/tts", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ text: message }),
                    });
                    const blob = await response.blob();
                    const url = URL.createObjectURL(blob);
                    audio = new Audio(url);
                    audio.play();
                    playing = true;
                    speakerBtn.textContent = "⏸️";

                    audio.addEventListener("ended", () => {
                        playing = false;
                        speakerBtn.textContent = "🔊";
                        audio = null;
                    });
                } catch (err) {
                    console.error("TTS error:", err);
                    alert("Could not play TTS.");
                }
            } else if (playing) {
                audio.pause();
                playing = false;
                speakerBtn.textContent = "🔊";
            } else {
                audio.play();
                playing = true;
                speakerBtn.textContent = "⏸️";
            }
        });

        msgDiv.appendChild(speakerBtn);
    }

    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

// -------------------- Send user message --------------------
async function sendMessage() {
    const message = userInput.value.trim();
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

    } catch (error) {
        console.error(error);
        appendMessage("Sorry, something went wrong. Try again.", "bot");
    }
}

// -------------------- Event listeners --------------------
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});

// -------------------- Voice input --------------------
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    micBtn.addEventListener("click", () => recognition.start());

    recognition.addEventListener("result", (e) => {
        userInput.value = e.results[0][0].transcript;
        sendMessage();
    });

    recognition.addEventListener("error", (e) => {
        console.error("Voice recognition error:", e.error);
        alert("Voice input failed. Try again.");
    });
} else {
    micBtn.addEventListener("click", () => {
        alert("Your browser does not support speech recognition.");
    });
}

// -------------------- Left-panel carousel --------------------
document.addEventListener("DOMContentLoaded", () => {
    const images = document.querySelectorAll(".left-panel .carousel img");
    let current = 0;

    function rotateImages() {
        images[current].classList.remove("active");
        current = (current + 1) % images.length;
        images[current].classList.add("active");
    }

    setInterval(rotateImages, 3000);
});
