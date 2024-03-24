//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

const API_KEY = "API_KEY";

// Información predefinida
const predefinedInfo = "Para ingresar a la pagina web debe ingresar al link comidarapida.com ";

async function getCompletion(prompt) {
  // Agrega la información predefinida al prompt
  const fullPrompt = predefinedInfo + prompt;

  const response = await fetch(`https://api.openai.com/v1/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({
      model: "text-davinci-003",
      prompt: fullPrompt,
      max_tokens: 50,
    }),
  });

  const data = await response.json();
  return data;
}

const promptInput = document.querySelector("#prompt");
const button = document.querySelector("#generate");
const output = document.querySelector("#output");

button.addEventListener("click", async () => {
  if (!promptInput.value) window.alert("Please enter a prompt");

  const response = await getCompletion(promptInput.value);
  output.innerHTML = response.choices[0].text;
});
