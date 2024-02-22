const companyDescription = {
  mainInfo:
    "Anncom - это 1-й маркетплейс операторов связи. Через наш портал можно выбрать телеком –решения, наиболее подходящие для вашего бизнеса",
  description: "Голосовой робот Бот N. :",
  list: [
    "Использует нейронные сети для построения расширенного анализа ответа Человека. Искусственный Интеллект извлекает" +
      "информацию из текста для получения вопроса или построения логического ответа(вывода) и способен на диалог с человеком." +
      "Робота Бот N. можно перебивать в диалоге, он слушает и отвечает.",
    "Использует внешние облачные технологии распознавания и синтеза речи Yandex SpeechKit",
    "Возможность бесплатно и без абонентской платы подключить любого оператора связи",
    "Взаимодействует по API с любой CRM-системой, Виртуальной АТС, CMS (корпоративным сайтом), ER",
  ],
  present:
    "🎁 Подарок для ДРУЗЕЙ – автоинформирование с " +
    "помощью голосового робота Бот N. - 100 клиентов по " +
    "вашей базе – текст сообщения разработаем " +
    "индивидуально, голос у робота может быть ваш! Отчёт с " +
    " распознанными ответами будет направлен для изучения" +
    "после обзвона",
};

const companyTasks = {
  mainInfo:
    "Бот N. - это голосовой робот, который поможет автоматизировать исходящие звонки; повысить лояльность, собирая отзывы и оценки; экономит временные и денежные затраты.",
  description: "С помощью Бот N. можно решить такие бизнес-задачи как:",
  list: [
    "Принимать заказы и уведомлять о доставке",
    "Уведомлять об акциях и информировать о специальных предложениях",
    "Актуализировать / фильтровать базу номеров",
    "Генерировать лиды",
    "Подтверждать бронь, встречу или запись к врачу",
    "Проводить социальные опросы или анкетирование",
    "Автоматизировать прием входящих звонков, а так же прием показаний счетчиков",
  ],
  present:
    "Систему автообзвона Бот N. сейчас может внедрить любая организация, которой необходимо увеличить скорость обработки входящих обращений или передачу исходящей информации",
};

function ucFirst(str) {
  if (!str) return str;
  return str[0].toUpperCase() + str.slice(1);
}
function main() {
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

  const boxButtonOrder = document.createElement("div");
  boxButtonOrder.className = "box-button right";

  const order = document.createElement("button");
  order.className = "order";
  order.textContent = "Какие задачи можно решить";

  order.addEventListener("click", () => {
    tasksDescription();
  });

  boxButtonOrder.append(order);

  box.append(mainInfo, description, list, present);

  mainDescription.append(box, boxButtonOrder);
  document.body.append(mainDescription);
}

main();

function tasksDescription() {
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
  mainInfo.textContent = companyTasks.mainInfo;

  const description = document.createElement("p");
  description.textContent = companyTasks.description;

  const present = document.createElement("p");
  present.textContent = companyTasks.present;

  const list = document.createElement("ul");
  for (const elem of companyTasks.list) {
    const elementList = document.createElement("li");
    elementList.textContent = ucFirst(elem);
    list.append(elementList);
  }

  const boxButtonBack = document.createElement("div");
  boxButtonBack.className = "box-button";

  const backButton = document.createElement("button");
  backButton.className = "back";
  backButton.textContent = "Вернуться";
  backButton.addEventListener("click", () => {
    main();
  });

  boxButtonBack.append(backButton);
  mainDescription.append(boxButtonBack);

  box.append(mainInfo, description, list, present);

  mainDescription.append(box);
  document.body.append(mainDescription);
}
