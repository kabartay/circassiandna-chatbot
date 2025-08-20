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
    init: function ({ apiUrl, containerId, onMessage, onTyping }) {
        const container = document.getElementById(containerId);
        if (!container) return;

        // Create ONLY the input row - remove the old chatlog structure
        container.innerHTML = `
            <div class="cw-input-row">
                <input type="text" id="userInput" placeholder="Ask me something...">
                <button id="sendBtn">Send</button>
            </div>
        `;

        const input = container.querySelector("#userInput");
        const button = container.querySelector("#sendBtn");

        const sendMessage = async () => {
            const message = input.value.trim();
            if (!message) return;

            // Add user message using callback
            if (onMessage) {
                onMessage(message, 'user');
            }

            input.value = '';

            // Show typing indicator
            if (onTyping) {
                onTyping();
            }

            try {
                const response = await fetch(apiUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: message }),
                });

                if (!response.ok) throw new Error("Network error");

                const data = await response.json();

                // Add bot response using callback
                if (onMessage) {
                    onMessage(data.answer, 'bot');
                }

            } catch (err) {
                console.error('Chat widget error:', err);

                // Add error message using callback
                if (onMessage) {
                    onMessage('Sorry, an error occurred. Please try again.', 'bot');
                }
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

        // Auto-focus on input when widget loads
        setTimeout(() => {
            input.focus();
        }, 100);

        // Return object with utility methods
        return {
            sendMessage,
            focusInput: () => input.focus(),
            clearInput: () => input.value = '',
            setPlaceholder: (text) => input.placeholder = text
        };
    }
};