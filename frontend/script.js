const form = document.getElementById("command-form");
const result = document.getElementById("result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const query = document.getElementById("query").value;

  const response = await fetch("/api/v1/commands", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: query,
    }),
  });

  const data = await response.json();
  console.log(data);
  result.textContent = data.speech;
  const audio = new Audio(`data:${data.audio.format};base64,${data.audio.base64}`);
  audio.play();
});
