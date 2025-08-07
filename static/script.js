const agentCard = document.getElementById('agent-card');
const statusText = document.getElementById('status-text');
const form = document.getElementById('voice-form');

// TTS Handler
form.addEventListener('submit', function (e) {
  e.preventDefault();
  const text = document.getElementById('tts-input').value.trim();

  if (!text) return alert("Please enter some text.");

  agentCard.classList.add('listening');
  statusText.textContent = "Generating voice...";

  fetch('http://127.0.0.1:5000/generate-audio', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text })
  })
  .then(res => res.json())
  .then(data => {
    if (data.audio_url) {
      const audio = new Audio(data.audio_url);
      audio.play();
    } else {
      alert("Failed to generate audio.");
    }
  })
  .catch(err => {
    console.error(err);
    alert("Something went wrong.");
  })
  .finally(() => {
    agentCard.classList.remove('listening');
    statusText.textContent = "Listening...";
  });
});

// Echo Bot: Recorder
let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById("start-recording");
const stopBtn = document.getElementById("stop-recording");
const playback = document.getElementById("playback");

startBtn.addEventListener("click", async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

  mediaRecorder = new MediaRecorder(stream);
  audioChunks = [];

  mediaRecorder.ondataavailable = event => {
    audioChunks.push(event.data);
  };

  mediaRecorder.onstop = () => {
    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
    const audioUrl = URL.createObjectURL(audioBlob);
    playback.src = audioUrl;
  };

  mediaRecorder.start();
  startBtn.disabled = true;
  stopBtn.disabled = false;
});

stopBtn.addEventListener("click", () => {
  mediaRecorder.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
});


