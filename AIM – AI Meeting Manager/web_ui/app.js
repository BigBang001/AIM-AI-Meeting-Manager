async function fetchJSON(url, data){
    const resp = await fetch(url,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify(data)
    });
    return resp.json();
}

function showWarning(msg){
    const warning = document.getElementById("promptWarning");
    warning.innerText = msg || "";
}

function renderMemory(data){
    document.getElementById("memoryBar").innerText = data.memory_bar;

    ["active","finalized","pinned"].forEach(section=>{
        const container = document.getElementById(section+"Container");
        container.innerHTML="";
        data[section].forEach((e,i)=>{
            const time = new Date(e.timestamp).toLocaleTimeString();
            const responses = e.responses.join(" / ");
            const div = document.createElement("div");
            div.className="prompt-entry";
            if(e.finalized) div.classList.add("finalized");
            if(e.pinned) div.classList.add("pinned");
            div.innerHTML=`<strong>${e.finalized ? "FINALIZED":"ACTIVE"} - ${e.prompt}</strong> → ${responses} (${time}) <button>Pin</button>`;
            const btn = div.querySelector("button");
            btn.addEventListener("click", ()=> pin(i));
            container.appendChild(div);
        });
    });

    updateRecap();
}

async function addPrompt(){
    showWarning("");
    const prompt=document.getElementById("promptInput").value.trim();
    if(!prompt) return showWarning("Please enter a prompt!");
    const data = await fetchJSON("/add_prompt",{prompt});
    if(data.error) return showWarning(data.error);
    renderMemory(data);
    document.getElementById("promptInput").value="";
}

async function undo(){
    const data = await fetchJSON("/undo", {});
    if(data.warning) showWarning(data.warning);
    renderMemory(data);
}

async function finalize(){
    const data = await fetchJSON("/finalize", {});
    if(data.message) showWarning(data.message);
    renderMemory(data);
}

async function pin(index){
    const data = await fetchJSON("/pin",{index});
    renderMemory(data);
}

// Dark/Light toggle
const toggle = document.getElementById("toggleTheme");
toggle.addEventListener("click",()=>{
    document.body.classList.toggle("dark-mode");
    toggle.innerText = document.body.classList.contains("dark-mode") ? "☀️ Light Mode" : "🌙 Dark Mode";
});

async function updateRecap(){
    const resp = await fetch("/recap");
    const data = await resp.json();
    const container = document.getElementById("recapContainer");
    container.innerHTML = "";
    data.recap.forEach(entry=>{
        const div = document.createElement("div");
        div.className = "prompt-entry";
        div.innerText = entry;
        container.appendChild(div);
    });
}
