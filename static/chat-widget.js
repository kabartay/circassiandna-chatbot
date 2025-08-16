// static/chat-widget.js

// ---------------------------
// Circassian DNA Chat Widget
// ---------------------------

window.ChatWidget = {
    init: function ({ apiUrl, containerId }) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div id="chatlog" style="border:1px solid #ccc; height:200px; overflow:auto; padding:10px;"></div>
            <input type="text" id="userInput" placeholder="Ask me something..." style="width:80%;">
            <button id="sendBtn">Send</button>
        `;

        const chatlog = container.querySelector("#chatlog");
        const input = container.querySelector("#userInput");
        const button = container.querySelector("#sendBtn");

        const sendMessage = async () => {
            const message = input.value.trim();
            if (!message) return;
            chatlog.innerHTML += `<div><b>You:</b> ${message}</div>`;
            input.value = '';

            try {
                const response = await fetch(apiUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: message }),
                });
                if (!response.ok) throw new Error("Network error");
                const data = await response.json();
                chatlog.innerHTML += `<div><b>Bot:</b> ${data.answer}</div>`;
                chatlog.scrollTop = chatlog.scrollHeight;
            } catch (err) {
                chatlog.innerHTML += `<div><b>Bot:</b> Sorry, error occurred.</div>`;
                console.error(err);
            }
        };

        // Button click
        button.onclick = sendMessage;

        // Press Enter key
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                sendMessage();
            }
        });
    }
};
