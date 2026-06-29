const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const resetBtn = document.getElementById("resetBtn");
const sentimentDisplay = document.getElementById("sentimentDisplay");
const meterBar = document.getElementById("meterBar");
const explanationBox = document.getElementById("explanationBox");
const profileBox = document.getElementById("profileBox");

let isLoading = false;
let userProfile = {};

// Auto-resize textarea
userInput.addEventListener("input", () => {
    userInput.style.height = "auto";
    userInput.style.height = Math.min(userInput.scrollHeight, 120) + "px";
});

// Send on Enter (Shift+Enter for newline)
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener("click", sendMessage);
resetBtn.addEventListener("click", resetChat);

function addMessage(content, role) {
    const div = document.createElement("div");
    div.className = `message ${role}-message`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = role === "bot" ? "🤖" : "👤";

    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";
    contentDiv.innerHTML = formatMarkdown(content);

    div.appendChild(avatar);
    div.appendChild(contentDiv);
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.*?)\*/g, "<em>$1</em>")
        .replace(/\n/g, "<br>")
        .split(/(?:<br>){2,}/)
        .map(p => `<p>${p}</p>`)
        .join("");
}

function showTyping() {
    const div = document.createElement("div");
    div.className = "message bot-message";
    div.id = "typingIndicator";
    div.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="typing-indicator">
            <span></span><span></span><span></span>
        </div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTyping() {
    const el = document.getElementById("typingIndicator");
    if (el) el.remove();
}

function updateSentiment(sentiment) {
    sentimentDisplay.innerHTML = `
        <span class="sentiment-emoji">${sentiment.emoji}</span>
        <span class="sentiment-label">${sentiment.label} (${(sentiment.score * 100).toFixed(0)}%)</span>`;

    const percent = ((sentiment.polarity + 1) / 2) * 100;
    meterBar.style.width = percent + "%";
}

function updateExplanation(explanation) {
    if (explanation.factors && explanation.factors.length > 0) {
        explanationBox.innerHTML =
            "<ul>" +
            explanation.factors.map(f => `<li>🔍 ${f}</li>`).join("") +
            "</ul>";
    }
}

function updateProfile(data) {
    // Build profile display from accumulated chat data
    if (data.sentiment) {
        userProfile.lastSentiment = data.sentiment.label;
    }
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message || isLoading) return;

    isLoading = true;
    sendBtn.disabled = true;

    addMessage(message, "user");
    userInput.value = "";
    userInput.style.height = "auto";
    showTyping();

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });
        const data = await res.json();

        removeTyping();

        if (data.error) {
            addMessage("Something went wrong. Please try again.", "bot");
        } else {
            addMessage(data.response, "bot");
            updateSentiment(data.sentiment);
            updateExplanation(data.explanation);
            updateProfile(data);
        }
    } catch (err) {
        removeTyping();
        addMessage("Connection error. Please check your server.", "bot");
    }

    isLoading = false;
    sendBtn.disabled = false;
    userInput.focus();
}

async function resetChat() {
    await fetch("/reset", { method: "POST" });
    chatMessages.innerHTML = "";
    addMessage(
        "Welcome back! I've reset our conversation. " +
        "What would you like to explore in the world of automotive and motorsport?",
        "bot"
    );
    sentimentDisplay.innerHTML =
        '<span class="sentiment-emoji">😐</span>' +
        '<span class="sentiment-label">Awaiting input...</span>';
    meterBar.style.width = "50%";
    explanationBox.innerHTML = "<p>Explanations will appear here after your first message.</p>";
    profileBox.innerHTML = "<p>Start chatting to build your profile.</p>";
    userProfile = {};
}