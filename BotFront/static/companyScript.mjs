const companyDescription = {
  mainInfo:
    "Компания ANNCOM (АННКОМ) – это команда ИТ-специалистов и разработчиков, способных решить внутренние технические и финансовые задачи в ИТ сегменте вашей организации.",
  description: "Направление деятельности:",
  list: [
    "Телефония. Выбор поставщика ip-телефонии. Оптимизация трафика и сокращение расходов. Интеграция с внешними системами. Установка и внедрение серверных АТС.",
    "Рекомендации по выбору ip-оборудования",
    "ИТ-аудит и консалтинг. Скорая ИТ-помощь",
    "Собственная разработка – Голосовой робот Бот N.",
  ],
  present:
    "⚠️ Предусмотрены готовые решения по оптимизации процессов уведомлений, оповещений, автоинформирования, анкетирования, приглашений и подтверждений, лидогенерации." +
    "Посмотрите коробки и выберете свою!",
};

function ucFirst(str) {
  if (!str) return str;
  return str[0].toUpperCase() + str.slice(1);
}

if (document.querySelector(".mainBox")) {
  const mainDescription = document.querySelector(".mainBox");
  mainDescription.remove();
}

const mainDescription = document.createElement("div");
mainDescription.className = "mainBox main-description";

const box = document.createElement("div");
box.className = "box";

const mainInfo = document.createElement("p");
mainInfo.className = "headline";
mainInfo.textContent = companyDescription.mainInfo;

const description = document.createElement("p");
description.textContent = companyDescription.description;

const present = document.createElement("p");
present.textContent = companyDescription.present;

const list = document.createElement("ul");
for (const elem of companyDescription.list) {
  const elementList = document.createElement("li");
  elementList.textContent = ucFirst(elem);
  list.append(elementList);
}

box.append(mainInfo, description, list, present);

mainDescription.append(box);
document.body.append(mainDescription);
