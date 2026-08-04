const CHAT_API_URL = "http://192.168.40.39:8000/chat";
const GET_API_URL = "http://192.168.40.39:8000/get_history";
const TTS_API_URL = "http://192.168.40.39:8000/tts";

const chat = document.getElementById("chat");
const input = document.getElementById("message");
const whisper = document.getElementById("whisper");
is_async = false;
is_whisper = false;

async function load(){

    if(is_async){
        return;
    }

    try{
        is_async = true;

        const response = await fetch(GET_API_URL);
        const history = await response.json();

        history.forEach(h => {
            if (h.role === "user") 
                name = "あなた";
            else
                name = "ミオ";
            appendMessage(name, h.content, h.role);
        });

    }
    catch(e){

        appendMessage(
            "System",
            "通信エラー",
            "assistant"
        );

    }
    is_async = false;
}

async function sendMessage(){

    if(is_async){
        return;
    }

    const text = input.value.trim();

    if(text === ""){
        return;
    }

    appendMessage("あなた", text, "user");

    input.value = "";

    try{
        is_async = true;

        const response = await fetch(CHAT_API_URL,{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:text
            })

        });

        const json = await response.json();

        appendMessage("ミオ", json.reply, "assistant");
        await playVoice(json.reply, json.emotion);

    }
    catch(e){

        appendMessage(
            "System",
            "通信エラー",
            "assistant"
        );

    }
    is_async = false;
}

async function playVoice(text, emotion){

    try{
        const response = await fetch(TTS_API_URL,{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:text,
                emotion:emotion,
                is_whisper:is_whisper
            })

        });

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        await audio.play();
        audio.onended = () => URL.revokeObjectURL(url);
    }
    catch(e){
        console.error("音声再生エラー:", e);
    }
}

function appendMessage(name, message, css){

    chat.innerHTML +=
    `<div class="${css}">
        <b>${name}</b><br>
        ${message}
    </div>`;

    chat.scrollTop = chat.scrollHeight;

}

function change_whisper(){

    is_whisper = is_whisper ? false : true;
    if (is_whisper) {
        whisper.style.backgroundColor = "#acacac";
    } else {
        whisper.style.backgroundColor = "#1976D2";
    }

}

window.onload = async function () {
    await load();
}
