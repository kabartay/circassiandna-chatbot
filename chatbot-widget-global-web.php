add_action('wp_footer', function() {
?>
<style>
/* Chat container - Expanded to almost full window */
#chatbot {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: calc(100vw - 40px);
    height: calc(100vh - 40px);
    max-width: 1200px;
    border: none;
    border-radius: 20px;
    background: #fff;
    display: none;
    flex-direction: column;
    overflow: hidden;
    z-index: 9999;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

/* Show when active */
#chatbot.active {
    display: flex;
}
	
/* Header */
#chatbot-header {
    background: linear-gradient(135deg, #567675, #4a625f);
    color: #fff;
    padding: 25px;
    font-weight: 600;
    text-align: center;
    font-size: 20px;
    position: relative;
    flex-shrink: 0;
    border-radius: 20px 20px 0 0;
}
	
/* Close button */
#chatbot-close {
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    font-weight: bold;
    font-size: 20px;
    background: rgba(255,255,255,0.2);
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

#chatbot-close:hover {
    background: rgba(255,255,255,0.3);
    transform: translateY(-50%) scale(1.1);
}

/* Messages container - Takes up most space, remove old chatlog styling */
#chatbot-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 25px;
    overflow-y: auto;
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    min-height: 0; /* Important for flex */
}

/* Remove old chatlog styling completely */
#chatlog {
    border: none !important;
    height: auto !important;
    overflow: visible !important;
    padding: 0 !important;
    background: transparent !important;
}

/* Messages area */
#chatbot-messages {
    display: flex;
    flex-direction: column;
    gap: 15px;
    min-height: 100%;
    justify-content: flex-end;
}

/* Custom scrollbar */
#chatbot-container::-webkit-scrollbar {
    width: 8px;
}

#chatbot-container::-webkit-scrollbar-track {
    background: transparent;
}

#chatbot-container::-webkit-scrollbar-thumb {
    background: rgba(86, 118, 117, 0.3);
    border-radius: 10px;
}

#chatbot-container::-webkit-scrollbar-thumb:hover {
    background: rgba(86, 118, 117, 0.5);
}

/* Chat bubbles - Proper styling */
.chat-message {
    max-width: 75%;
    padding: 15px 20px;
    border-radius: 20px;
    font-size: 16px;
    line-height: 1.5;
    word-wrap: break-word;
    position: relative;
    opacity: 0;
    transform: translateY(20px);
    animation: slideInMessage 0.4s ease-out forwards;
}

.chat-message.user {
    background: linear-gradient(135deg, #567675, #4a625f);
    color: #fff;
    align-self: flex-end;
    border-bottom-right-radius: 6px;
    box-shadow: 0 4px 15px rgba(86, 118, 117, 0.3);
}

.chat-message.bot {
    background: #fff;
    color: #333;
    align-self: flex-start;
    border-bottom-left-radius: 6px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border: 1px solid rgba(86, 118, 117, 0.1);
}

@keyframes slideInMessage {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Typing indicator */
.typing {
    background: #fff;
    color: #666;
    align-self: flex-start;
    border-radius: 20px 20px 20px 6px;
    padding: 15px 20px;
    font-style: italic;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border: 1px solid rgba(86, 118, 117, 0.1);
    opacity: 0;
    animation: slideInMessage 0.4s ease-out forwards;
}

.typing::after {
    content: '';
    animation: typingDots 1.4s infinite;
}

@keyframes typingDots {
    0%, 20% { content: '.'; }
    40% { content: '..'; }
    60%, 100% { content: '...'; }
}

/* Input container - Replace the basic input styling */
.cw-input-row {
    padding: 25px !important;
    background: #fff !important;
    border-top: 1px solid rgba(86, 118, 117, 0.1) !important;
    flex-shrink: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 15px !important;
    border-radius: 0 0 20px 20px !important;
}

/* Input field styling */
.cw-input-row input,
#userInput {
    flex: 1 !important;
    height: 55px !important;
    padding: 0 25px !important;
    border-radius: 30px !important;
    border: 2px solid #e9ecef !important;
    font-size: 16px !important;
    outline: none !important;
    transition: all 0.3s ease !important;
    font-family: inherit !important;
    background: #f8f9fa !important;
    width: auto !important; /* Override the 80% width */
}

.cw-input-row input:focus,
#userInput:focus {
    border-color: #567675 !important;
    background: #fff !important;
    box-shadow: 0 0 0 3px rgba(86, 118, 117, 0.1) !important;
}

/* Button styling */
.cw-input-row button,
#sendBtn {
    height: 55px !important;
    padding: 0 30px !important;
    border-radius: 30px !important;
    background: linear-gradient(135deg, #567675, #4a625f) !important;
    color: #fff !important;
    border: none !important;
    cursor: pointer !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    box-shadow: 0 4px 15px rgba(86, 118, 117, 0.3) !important;
    transition: all 0.3s ease !important;
    font-family: inherit !important;
}

.cw-input-row button:hover,
#sendBtn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(86, 118, 117, 0.4) !important;
}

.cw-input-row button:active,
#sendBtn:active {
    transform: translateY(0) !important;
}

/* Chat toggle button */
#chatbot-toggle {
    position: fixed;
    bottom: 25px;
    right: 25px;
    background: linear-gradient(135deg, #567675, #4a625f);
    color: #fff;
    padding: 18px 25px;
    border-radius: 50px;
    cursor: pointer;
    z-index: 10000;
    font-weight: 600;
    font-size: 16px;
    box-shadow: 0 8px 25px rgba(86, 118, 117, 0.4);
    transition: all 0.3s ease;
    border: none;
}

#chatbot-toggle:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 12px 30px rgba(86, 118, 117, 0.5);
}

/* Responsive design */
@media (max-width: 768px) {
    #chatbot {
        width: calc(100vw - 20px);
        height: calc(100vh - 20px);
        bottom: 10px;
        right: 10px;
        border-radius: 15px;
    }
    
    #chatbot-header {
        padding: 20px;
        font-size: 18px;
        border-radius: 15px 15px 0 0;
    }
    
    #chatbot-container {
        padding: 20px;
    }
    
    .chat-message {
        max-width: 85%;
        font-size: 15px;
        padding: 12px 16px;
    }
    
    .cw-input-row {
        padding: 20px !important;
        border-radius: 0 0 15px 15px !important;
    }
    
    .cw-input-row input,
    .cw-input-row button {
        height: 50px !important;
    }
}

@media (max-width: 480px) {
    #chatbot {
        width: 100vw;
        height: 100vh;
        bottom: 0;
        right: 0;
        border-radius: 0;
    }
    
    #chatbot-header {
        border-radius: 0;
    }
    
    .cw-input-row {
        border-radius: 0 !important;
    }
}
</style>

<div id="chatbot">
    <div id="chatbot-header">
        🧬 Chat with us!
        <div id="chatbot-close">&times;</div>
    </div>
    <div id="chatbot-container">
        <div id="chatbot-messages"></div>
    </div>
</div>

<div id="chatbot-toggle">💬 Chat</div>

<script src="https://circassiandna-chatbot.onrender.com/static/chat-widget.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
    const chatbox = document.getElementById('chatbot');
    const toggle = document.getElementById('chatbot-toggle');
    const closeBtn = document.getElementById('chatbot-close');
    const messages = document.getElementById('chatbot-messages');

    // Toggle chat visibility
    toggle.addEventListener('click', () => {
        chatbox.classList.toggle('active');
        if (chatbox.classList.contains('active')) {
            chatbox.style.display = 'flex';
            toggle.style.display = 'none';
            // Focus on input after opening
            setTimeout(() => {
                const input = document.querySelector('#userInput');
                if (input) input.focus();
            }, 100);
        } else {
            chatbox.style.display = 'none';
            toggle.style.display = 'block';
        }
    });

    // Close chat functionality
    closeBtn.addEventListener('click', () => {
        chatbox.classList.remove('active');
        chatbox.style.display = 'none';
        toggle.style.display = 'block';
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

    // Helper functions
    function addMessage(text, sender) {
        const bubble = document.createElement('div');
        bubble.className = `chat-message ${sender}`;
        bubble.textContent = text;
        messages.appendChild(bubble);
        
        // Smooth scroll to bottom
        setTimeout(() => {
            messages.scrollTop = messages.scrollHeight;
        }, 100);
    }

    function showTypingIndicator() {
        if (!document.querySelector('.typing')) {
            const typing = document.createElement('div');
            typing.className = 'typing';
            typing.textContent = 'Bot is typing';
            messages.appendChild(typing);
            
            setTimeout(() => {
                messages.scrollTop = messages.scrollHeight;
            }, 100);
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
