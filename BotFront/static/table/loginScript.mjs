const selectTable = document.getElementById("tableSelect").value;
let body = 0;

if (selectTable == "Пользователи, зашедшие в бота") {
  body = 1;
}
async function sendSwitch() {
  try {
    let response = await fetch("/login_admin", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      throw Error(response.statusText);
    } else {
      console.log(response);
    }
    if (!response.ok) {
      alert("Ошибка");
      throw Error(response.statusText);
    } else {
      console.log(response);
    }
  } catch {}
}

sendSwitch();
