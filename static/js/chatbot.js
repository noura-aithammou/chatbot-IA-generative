document.addEventListener('DOMContentLoaded', function() {
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotContainer = document.getElementById('chatbot-container');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const messagesContainer = document.getElementById('chatbot-messages');
    const fileInput = document.getElementById('file-input');
    const fileButton = document.getElementById('file-button');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    // Toggle chatbot expansion
    chatbotToggle.addEventListener('click', function() {
        chatbotContainer.classList.toggle('expanded');
        chatbotToggle.innerHTML = chatbotContainer.classList.contains('expanded') ? 
            '<i class="fas fa-chevron-down"></i>' : 
            '<i class="fas fa-chevron-up"></i>';
        
        // If expanding the chatbot, show welcome message if it's the first time
        if (chatbotContainer.classList.contains('expanded') && messagesContainer.children.length === 0) {
            addBotMessage(translations.chatbot_welcome);
        }
    });
    
    // Handle file button click
    fileButton.addEventListener('click', function() {
        fileInput.click();
    });
    
    // Show filename when a file is selected
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            const fileName = fileInput.files[0].name;
            addUserMessage(`${translations.file_selected}: ${fileName}`);
        }
    });
    
    // Handle message submission
    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        const hasFile = fileInput.files.length > 0;
        
        if (!message && !hasFile) {
            return;
        }
        
        // Add user message to chat
        if (message) {
            addUserMessage(message);
        }
        
        // Clear input field
        messageInput.value = '';
        
        // Create FormData to send both text and file
        const formData = new FormData();
        formData.append('query', message);
        
        if (hasFile) {
            formData.append('image', fileInput.files[0]);
        }
        
        // Show loading indicator
        showLoading(true);
        
        // Send the message to the server
        fetch('/api/chat', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator
            showLoading(false);
            
            if (data.error) {
                addBotMessage(translations.error_occurred + ': ' + data.error);
            } else {
                addBotMessage(data.answer);
            }
            
            // Clear file input
            fileInput.value = '';
        })
        .catch(error => {
            // Hide loading indicator
            showLoading(false);
            console.error('Error:', error);
            addBotMessage(translations.error_occurred + ': ' + error.message);
            
            // Clear file input
            fileInput.value = '';
        });
    });
    
    // Add a message from the user to the chat
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        messageElement.textContent = message;
        messagesContainer.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Add a message from the bot to the chat
    function addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        messageElement.textContent = message;
        messagesContainer.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Show or hide loading indicator
    function showLoading(show) {
        loadingIndicator.style.display = show ? 'block' : 'none';
    }
    
    // Scroll the chat to the bottom
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});
