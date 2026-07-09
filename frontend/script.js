const SESSION_ID = "website-user";

// =========================
// AI CHAT
// =========================

async function sendMessage() {

    const input = document.getElementById("message");
    const text = input.value.trim();

    if (text === "") return;

    const messages = document.getElementById("messages");

    // Show user message
    messages.innerHTML += `
<div class="user">
    <div class="message-row right">
        <div class="bubble user-bubble">${text}</div>
        <div class="avatar">👤</div>
    </div>
</div>
`;

    input.value = "";
    messages.scrollTop = messages.scrollHeight;

    // AI typing
    const loadingId = "loading-" + Date.now();

    messages.innerHTML += `
<div class="bot" id="${loadingId}">
    <div class="message-row">
        <div class="avatar">🐾</div>

        <div class="bubble bot-bubble">

            <div class="typing">
                <span></span>
                <span></span>
                <span></span>
            </div>

        </div>
    </div>
</div>
`;

    messages.scrollTop = messages.scrollHeight;

    try {

        const response = await fetch("https://paw-spa-ai-agent.onrender.com/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                session_id: SESSION_ID,
                message: text
            })

        });

        const data = await response.json();

        document.getElementById(loadingId).innerHTML = `
<div class="message-row">
    <div class="avatar">🐾</div>
    <div class="bubble bot-bubble">
        ${data.reply}
    </div>
</div>
`;

speak(data.reply);

messages.scrollTop = messages.scrollHeight; 

    }

    catch (error) {

        document.getElementById(loadingId).innerHTML =
            `<span>❌ Error connecting to server.</span>`;

        console.error(error);

    }

}

// =========================
// QUICK ACTION BUTTONS
// =========================

function quickMessage(text) {

    document.getElementById("message").value = text;

    sendMessage();

}

// =========================
// BOOK APPOINTMENT
// =========================

async function bookAppointment() {

    const booking = {

        name: document.getElementById("name").value,
        phone: document.getElementById("phone").value,
        pet_name: document.getElementById("pet_name").value,
        pet_type: document.getElementById("pet_type").value,
        breed: document.getElementById("breed").value,
        service: document.getElementById("service").value,
        date: document.getElementById("date").value,
        time: document.getElementById("time").value

    };

    try {

        const response = await fetch("https://paw-spa-ai-agent.onrender.com/book", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(booking)

        });

        const data = await response.json();

        alert(data.message);

        // Clear form

        document.getElementById("name").value = "";
        document.getElementById("phone").value = "";
        document.getElementById("pet_name").value = "";
        document.getElementById("pet_type").value = "";
        document.getElementById("breed").value = "";
        document.getElementById("service").value = "";
        document.getElementById("date").value = "";
        document.getElementById("time").value = "";

    }

    catch (error) {

        alert("Unable to create booking.");

        console.error(error);

    }

}

// =========================
// VOICE AI
// =========================

function startListening() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        alert("Speech Recognition is not supported in this browser.");

        return;

    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onstart = () => {

        console.log("🎤 Listening...");

    };

    recognition.onresult = (event) => {

        const transcript = event.results[0][0].transcript;

        document.getElementById("message").value = transcript;

        sendMessage();

    };

    recognition.onerror = (event) => {

        console.error("Speech Error:", event.error);

        alert("Microphone Error: " + event.error);

    };

}

function speak(text) {

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";
    speech.rate = 1;
    speech.pitch = 1;
    speech.volume = 1;

    window.speechSynthesis.speak(speech);

}

function fillBookingForm(booking) {

    if (booking.name)
        document.getElementById("name").value = booking.name;

    if (booking.phone)
        document.getElementById("phone").value = booking.phone;

    if (booking.pet_name)
        document.getElementById("pet_name").value = booking.pet_name;

    if (booking.pet_type)
        document.getElementById("pet_type").value = booking.pet_type;

    if (booking.breed)
        document.getElementById("breed").value = booking.breed;

    if (booking.service)
        document.getElementById("service").value = booking.service;

    if (booking.date)
        document.getElementById("date").value = booking.date;

    if (booking.time)
        document.getElementById("time").value = booking.time;

}

function toggleChat(){

    const chat = document.getElementById("chatWindow");

    if(chat.style.display==="block"){

        chat.style.display="none";

    }else{

        chat.style.display="block";

    }

}

function sendWhatsApp() {

    const name = document.getElementById("name").value;
    const phone = document.getElementById("phone").value;
    const pet = document.getElementById("pet_name").value;
    const type = document.getElementById("pet_type").value;
    const breed = document.getElementById("breed").value;
    const service = document.getElementById("service").value;
    const date = document.getElementById("date").value;
    const time = document.getElementById("time").value;

    const message =
`Hello Paw Spa & Nest,

I would like to book an appointment.

Owner: ${name}
Phone: ${phone}
Pet: ${pet}
Type: ${type}
Breed: ${breed}
Service: ${service}
Date: ${date}
Time: ${time}`;

    const whatsappNumber = "919059430535";

    const url =
`https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;

    window.open(url, "_blank");
}