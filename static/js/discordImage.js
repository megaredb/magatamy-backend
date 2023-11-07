let card = document.getElementById("cardImageUser")

var users = {"493318176189448204": {}, "961256514427969607": {}, "513975760189390855": {}};

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
    <p class="card__name">${global_name}</p>
    <p class="card__p">Блогер</p>
    <ul class="social-icons">
      <li><a href="https://www.youtube.com/channel/UCdrZrlodik1odF5hrHr5w3Q" target="_blank"><ion-icon
            name="logo-youtube"></ion-icon></a></li>

    </ul>
  </div>
`
card.innerHTML=card.innerHTML+cardUser

})
}
for (var userId in users) {
  getUserCard(userId);
}