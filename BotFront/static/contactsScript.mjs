const contactsList = {
  head: "Автодайлер «Бот N.» автоматизация звонков",
  description:
    "✅ Бот N. — робот для автообзвона и обработки входящих звонков.",
  mainUrl: "🌐 www.anncom.ru/botn",
  phoneList: ["☎️ +74959900056", "☎️ +79336660056"],
  email: "📪 autodialer@anncom.ru",
  secondaryUrl: [
    "☑️ Конструктор для роботов:",
    "https://www.anncom.ru/constructor/",
    "☑️ Коробочные решения:",
    "https://www.anncom.ru/botn/#box",
  ],
};

const mainDescription = document.createElement("div");
mainDescription.className = "mainBox main-description";

const box = document.createElement("div");
box.className = "box";

const mainInfo = document.createElement("p");
mainInfo.className = "headline";
mainInfo.textContent = contactsList.head;

const description = document.createElement("p");
description.textContent = contactsList.description;

const mainUrl = document.createElement("p");
mainUrl.textContent = contactsList.mainUrl;

const email = document.createElement("p");
email.textContent = contactsList.email;

const phoneList = document.createElement("ul");
phoneList.className = "phoneList";

for (const elem of contactsList.phoneList) {
  const elementList = document.createElement("p");
  elementList.textContent = elem;
  phoneList.append(elementList);
}

const secondaryUrl = document.createElement("ul");
secondaryUrl.className = "phoneList";

for (const elem of contactsList.secondaryUrl) {
  const elementList = document.createElement("p");
  elementList.textContent = elem;
  phoneList.append(elementList);
}

box.append(mainInfo, description, mainUrl, phoneList, email, secondaryUrl);

mainDescription.append(box);
document.body.append(mainDescription);
