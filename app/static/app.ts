type EventItem = {
  event: "push" | "pull_request" | "merge";
  author: string;
  from_branch: string | null;
  to_branch: string;
  timestamp: string;
};

const list = document.getElementById("events") as HTMLUListElement


function formatEvent(e:EventItem){
    const time = new Date(e.timestamp).toUTCString()
    if (e.event==="push"){
        return `${e.author} pushed to ${e.to_branch} on ${time}`
    }
     if (e.event === "pull_request") {
    return `${e.author} submitted a pull request from "${e.from_branch}" to "${e.to_branch}" on ${time}`;
  }

  return `${e.author} merged branch "${e.from_branch}" to "${e.to_branch}" on ${time}`;
}

async function loadEvents(){
try{
    const result = await fetch("/events")
    const data:EventItem[] = await result.json()
    if (!list) return;
    list.innerHTML=""

    data.forEach((e)=>{
        const li = document.createElement("li")
        li.textContent=formatEvent(e)

        const timeDiv = document.createElement("div")
        timeDiv.className="time"
        timeDiv.textContent=new Date(e.timestamp).toUTCString()
        li.appendChild(timeDiv)
        list.appendChild(li)
    })
}catch(err){
     console.error("Failed to load events:", err);
}
}

loadEvents()
setInterval(loadEvents, 15000)