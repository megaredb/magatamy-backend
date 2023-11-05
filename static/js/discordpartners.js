let langData = [["Язык", "Language", "Мова"], ["Социальная сеть", "social network", "соціальні мережі"], ["Магазин", "shop", "крамниця"], ["Карта мира", "world map", "карта світу"], ["Вики", "Wiki", "Вікі"], ["Вход", "Entry", "Вхід"], ["Выживание с атмосферным комьюнити и уникальными фишками", "Survival with atmospheric community and unique features", "Виживання з атмосферним ком'юніті та унікальними фішками"], ["ИНФОРМАЦИЯ", "INFORMATION", "ІНФОРМАЦІЯ"], ["Советуем прочитать!", "You are advised to read it!", "Радимо прочитати!"], ["Моды и плагины", "", "Моди та плагіни"], ["Дополнительная информация о модификациях На нашем сервере внедрены модификации, которые придают игре уникальный и интересный характер. Если вы хотите узнать больше о каждой из них, посетите наш специальный дискорд канал **(ссылка на дискорд канал)** для подробных сведений.", "", "Додаткова інформація про модифікації На нашому сервері впроваджено модифікації, які надають грі унікальний і цікавий характер. Якщо ви хочете дізнатися більше про кожну з них, відвідайте наш спеціальний дискорд-канал **(посилання на дискорд-канал)** для докладних відомостей."]]

let langTags = document.getElementsByClassName("translate");

let card = document.getElementById("cardImageUser")

var users = { "493318176189448204": { userDesc: "API разработчик" }, "961256514427969607": { userDesc: "frondEnd разработчик" }, "513975760189390855": { userDesc: "Основатель проекта" }, "463661523181502464": { userDesc: "Блогер" }, "227117061011144704": { userDesc: "Правая рука" } };

function getUserCard(userId) {
  return fetch(`/api/v1/discord/users-by-bot/${userId}`)
    .then(response => response.json())
    .then(commits => {
      console.log(commits);
      let avatar = (commits.avatar);
      let global_name = (commits.global_name);
      let cardUser = `
    <div class="cardCommand">
    <img
      src="https://cdn.discordapp.com/avatars/${userId}/${avatar}.webp?size=128"
      alt="Person" class="card__image">
    <p class="card__name">${global_name}</p> <br>
    <p class="card__p">${users[userId].userDesc}</p>
    <ul class="social-icons">
      <li><a href="https://www.youtube.com/channel/UCdrZrlodik1odF5hrHr5w3Q" target="_blank"><ion-icon
            name="logo-youtube"></ion-icon></a></li>

    </ul>
  </div>
`
      card.innerHTML = card.innerHTML + cardUser

    })
}

function translateText(language) {
  let langIndex

  if (language == "RU") {
    langIndex = 0
  }
  else if (language == "US") {
    langIndex = 1
  }
  else {
    langIndex = 2
  }

  for (let i = 0; i < langTags.length; i++) {
    langTags[i].innerHTML = langData[i][langIndex]
  }


}

for (var userId in users) {
  getUserCard(userId);
}