const CHAT_API_URL = "http://192.168.40.39:8000/chat";
const GET_API_URL = "http://192.168.40.39:8000/get_history";

const chat = document.getElementById("chat");
const input = document.getElementById("message");
is_async = false;

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
        console.log(json);

        appendMessage("ミオ", json.reply, "assistant");

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

function appendMessage(name, message, css){

    chat.innerHTML +=
    `<div class="${css}">
        <b>${name}</b><br>
        ${message}
    </div>`;

    chat.scrollTop = chat.scrollHeight;

}