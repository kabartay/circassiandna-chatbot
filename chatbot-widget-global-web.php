add_action('wp_footer', function() {
?>
<style>
/* Chat container */
#chatbot {
    position: fixed;
    bottom: 80px;
    right: 20px;
    width: 350px;
    height: 500px;
    border: 1px solid #ccc;
    border-radius: 12px;
    background: #fff;
    display: none;
    flex-direction: column;
    overflow: hidden;
    z-index: 9999;
    font-family: Arial, sans-serif;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
	z-index: 9999; /* keep chat window under toggle button */
}

/* Show when active */
#chatbot.active {
    display: flex;
}
	
/* Header */
#chatbot-header {
    background: #567675; /* #0073aa; */
    color: #fff;
    padding: 12px;
    font-weight: bold;
    text-align: center;
    font-size: 16px;
}
	
/* Close button */
#chatbot-close {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    font-weight: bold;
    font-size: 16px;
}

/* Messages container */
#chatbot-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 10px;
    overflow-y: auto;
}

/* Chat bubbles */
.chat-message.user {
    background-color: #567675; /* #0073aa; */
    color: #fff;
    align-self: flex-end;
    border-radius: 20px 20px 5px 20px;
    margin-bottom: 8px;
    padding: 8px 12px;
    max-width: 80%;
    word-wrap: break-word;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    opacity: 0;
    transform: translateY(10px);
    animation: fadeInUp 0.2s forwards;
}

.chat-message.bot {
    background-color: #f1f1f1;
    color: #000;
    align-self: flex-start;
    border-radius: 20px 20px 20px 5px;
    margin-bottom: 8px;
    padding: 8px 12px;
    max-width: 80%;
    word-wrap: break-word;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    opacity: 0;
    transform: translateY(10px);
    animation: fadeInUp 0.2s forwards;
}

@keyframes fadeInUp {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Typing indicator */
.typing {
    font-style: italic;
    color: #555;
    margin-bottom: 8px;
    opacity: 0;
    animation: fadeInUp 0.2s forwards;
}

/* Chat toggle button */
#chatbot-toggle {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #567675; /* #0073aa; */
    color: #fff;
    padding: 8px 12px;
    border-radius: 8px 8px 0 0;
    cursor: pointer;
	z-index: 10000; /* higher than chatbox */
}
</style>

<div id="chatbot">
    <div id="chatbot-header">Chat with us!</div>
    <div id="chatbot-container">
        <div id="chatbot-messages"></div>
    </div>
</div>

<div id="chatbot-toggle">Chat</div>

<script src="https://circassiandna-chatbot.onrender.com/static/chat-widget.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
    const chatbox = document.getElementById('chatbot');
    const toggle = document.getElementById('chatbot-toggle');
    const messages = document.getElementById('chatbot-messages');

    // Toggle chat visibility
	toggle.addEventListener('click', () => {
		chatbox.classList.toggle('active');
		if (chatbox.classList.contains('active')) {
			chatbox.style.display = 'flex';
		} else {
			chatbox.style.display = 'none';
		}
	});


    // Initialize ChatWidget
    ChatWidget.init({
        apiUrl: 'https://circassiandna-chatbot.onrender.com/api/chat',
        containerId: 'chatbot-messages',
        onMessage: (msg, sender) => {
            removeTypingIndicator();
            addMessage(msg, sender);
        },
        onTyping: () => {
            showTypingIndicator();
        }
    });

    // MutationObserver to style input row & add Enter key sending
    const container = document.getElementById('chatbot-container');
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === 1 && node.classList.contains('cw-input-row')) {
                    node.style.display = 'flex';
                    node.style.alignItems = 'center';
                    node.style.gap = '8px';
                    const input = node.querySelector('input');
                    const button = node.querySelector('button');
                    if (input && button) {
                        // Style input
                        input.style.flex = '1';
                        input.style.height = '45px';
                        input.style.padding = '0 15px';
                        input.style.borderRadius = '25px';
                        input.style.border = '1px solid #ccc';
                        input.style.fontSize = '14px';
                        // Style button
                        button.style.height = '45px';
                        button.style.padding = '0 20px';
                        button.style.borderRadius = '25px';
                        button.style.backgroundColor = '#567675'; // #0073aa
                        button.style.color = '#fff';
                        button.style.border = 'none';
                        button.style.cursor = 'pointer';
						button.style.boxShadow = '0 2px 6px rgba(86, 118, 117, 0.5)';
						// button.style.boxShadow = '0 2px 6px rgba(0,0,0,0.1)';

                        // Add "send on Enter" functionality
                        input.addEventListener('keydown', e => {
                            if (e.key === 'Enter') {
                                e.preventDefault();
                                button.click();
                            }
                        });
                    }
                }
            });
        });
    });
    observer.observe(container, { childList: true, subtree: true });

    // Helper functions
    function addMessage(text, sender) {
        const bubble = document.createElement('div');
        bubble.className = `chat-message ${sender}`;
        bubble.textContent = text;
        messages.appendChild(bubble);
        messages.scrollTop = messages.scrollHeight;
    }

    function showTypingIndicator() {
        if (!document.querySelector('.typing')) {
            const typing = document.createElement('div');
            typing.className = 'typing';
            typing.textContent = 'Bot is typing...';
            messages.appendChild(typing);
            messages.scrollTop = messages.scrollHeight;
        }
    }

    function removeTypingIndicator() {
        const typing = document.querySelector('.typing');
        if (typing) typing.remove();
    }
});
</script>
<?php
});
