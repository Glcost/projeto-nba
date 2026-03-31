
    // Faz as mensagens sumirem sozinhas após 5 segundos
    setTimeout(() => {
        const messages = document.querySelectorAll('[id^="flash-message-"]');
        messages.forEach(msg => {
        msg.style.opacity = '0';
    msg.style.transition = 'opacity 0.5s ease';
            setTimeout(() => msg.remove(), 500);
        });
    }, 5000);
