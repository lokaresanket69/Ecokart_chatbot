const messagesDiv = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function appendMessage(text, sender) {
    const msg = document.createElement('div');
    msg.classList.add('msg', sender);
    msg.textContent = text;
    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

sendBtn.onclick = async function() {
    const text = userInput.value.trim();
    if (!text) return;
    appendMessage(text, 'user');
    userInput.value = '';
    appendMessage('...', 'bot');
    try {
        const res = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        messagesDiv.lastChild.textContent = data.response;
    } catch (e) {
        messagesDiv.lastChild.textContent = 'Error connecting to chatbot.';
    }
};

userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') sendBtn.onclick();
});

// init particles
window.onload = () => {
  tsParticles.load("tsparticles", {
    fpsLimit: 60,
    background: { color: "transparent" },
    particles: {
      number: { value: 40 },
      color: { value: ["#43c06d", "#29984a", "#ffffff"] },
      shape: { type: "circle" },
      opacity: { value: 0.3 },
      size: { value: { min: 1, max: 4 } },
      move: { enable: true, speed: 1.2, direction: "none", outModes: "bounce" }
    },
    interactivity: {
      events: { onHover: { enable: true, mode: "repulse" }, resize: true },
      modes: { repulse: { distance: 80 } }
    },
    detectRetina: true
  });

  // Theme toggle
  const toggleBtn = document.getElementById("theme-toggle");
  let dark = false;
  toggleBtn.onclick = () => {
    dark = !dark;
    document.body.classList.toggle("dark-mode", dark);
    toggleBtn.textContent = dark ? "☀️" : "🌙";
  };
};

// Dark-mode styles injected via JS for brevity
const style = document.createElement("style");
style.textContent = `
  .dark-mode #chatbox { background:#1e1f26; box-shadow:0 8px 20px rgba(0,0,0,.6); }
  .dark-mode h2 { background:#29984a; }
  .dark-mode #messages{ background:#262835; }
  .dark-mode .bot{ background:#383c4d; color:#e1e1e1; }
  .dark-mode .user{ background:#29984a; }
  .dark-mode #user-input{ background:#12131a; color:#e1e1e1; border-color:#383c4d; }
`;
document.head.appendChild(style);
