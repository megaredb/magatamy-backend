document.addEventListener("DOMContentLoaded", function () {
    var staffContainers = document.querySelector(".staff-container");
    let staffCards = ``

    var staffs = {
        "227117061011144704": "Основатель проекта",
        "513975760189390855": "Правая рука",
        "493318176189448204": "API разработчик",
        "946480717813121024": "3D модельер",
        "818463159793745930": "Дизайнер"
    };

    function setUserCard(user) {
        return fetch(`/api/v1/discord/users-by-bot/${user}`)
            .then(response => response.json())
            .then(commits => {
                let staffAvatar = commits.avatar;
                let staffName = commits.username;
                let staffCard = `
                    <div class="staff-card">
                        <div class="staff-image">
                            <img src="https://cdn.discordapp.com/avatars/${user}/${staffAvatar}.webp?size=128" alt="Avatar STAFF">
                        </div>
                        <div class="staff-info">
                            <p class="staff-name">${staffName}</p>
                            <p class="staff-description">${staffs[user]}</p>
                        </div>
                    </div>
                `;
                return staffCard;
            });
    }

    Promise.all(Object.keys(staffs).map(user => setUserCard(user)))
        .then(cards => {
            staffContainers.innerHTML += cards.join('');
        });
});
