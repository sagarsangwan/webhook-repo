type EventItem = {
  event: "push" | "pull_request" | "merge";
  author: string;
  from_branch: string | null;
  to_branch: string;
  timestamp: string;
};

function timeAgo(isoDate: string): string {
  const now = new Date().getTime();
  const past = new Date(isoDate).getTime();
  const diff = Math.floor((now - past) / 1000);

  if (diff < 5) return "just now";
  if (diff < 60) return `${diff} seconds ago`;

  const minutes = Math.floor(diff / 60);
  if (minutes < 60) return `${minutes} minute${minutes > 1 ? "s" : ""} ago`;

  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} hour${hours > 1 ? "s" : ""} ago`;

  const days = Math.floor(hours / 24);
  if (days === 1) return "yesterday";
  if (days < 7) return `${days} days ago`;

  return new Date(isoDate).toLocaleDateString();
}

const list = document.getElementById("events") as HTMLUListElement;

function formatEvent(e: EventItem) {
  const time = new Date(e.timestamp).toUTCString();
  if (e.event === "push") {
    return `${e.author} pushed to ${e.to_branch} on ${time}`;
  }
  if (e.event === "pull_request") {
    return `${e.author} submitted a pull request from "${e.from_branch}" to "${e.to_branch}" on ${time}`;
  }

  return `${e.author} merged branch "${e.from_branch}" to "${e.to_branch}" on ${time}`;
}

async function loadEvents() {
  try {
    const result = await fetch("/events");
    const data: EventItem[] = await result.json();
    if (!list) return;
    list.innerHTML = "";

    data.forEach((e) => {
      const li = document.createElement("li");
      li.className = "event-item";

      const textDiv = document.createElement("div");
      textDiv.className = "event-text";
      textDiv.textContent = formatEvent(e);

      const timeDiv = document.createElement("div");
      timeDiv.className = "time";
      timeDiv.textContent = timeAgo(e.timestamp);

      li.appendChild(timeDiv);
      li.appendChild(textDiv);
      list.appendChild(li);
    });
  } catch (err) {
    console.error("Failed to load events:", err);
  }
}

loadEvents();
setInterval(loadEvents, 15000);
