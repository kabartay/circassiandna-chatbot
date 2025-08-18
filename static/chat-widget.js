// static/chat-widget.js

// ---------------------------
// Circassian DNA Chat Widget
// ---------------------------

/*
Copyright (C) 2025 Mukharbek Organokov
Website: www.circassiandna.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

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
