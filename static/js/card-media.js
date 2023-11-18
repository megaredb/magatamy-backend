document.addEventListener("DOMContentLoaded", function () {
    var mediaContainers = document.querySelector(".media-container");

    var medias = {
        "463661523181502464": {
            "description": "Любитель жаб",
            "socials": {
                "youtube": "https://www.youtube.com/@MegabyteY",
                "twitch": "https://www.twitch.tv/megabytey"
            }
        },
        "942492732797108244": {
            "description": "",
            "socials": {
                "youtube": "https://www.youtube.com/@xoxmach871"
            }
        },
        "1112736860221997076": {
            "description": "",
            "socials": {
                "youtube": "https://www.youtube.com/@gromlastday"
            }
        },
        "1114198957581664306": {
            "description": "",
            "socials": {
                "youtube": "https://www.youtube.com/@barsykEvgeny"
            }
        },
        "677193639423639553": {
            "description": "",
            "socials": {
                "youtube": "https://www.youtube.com/@Luriking"
            }
        }
    };

    function setUserCard(user) {
        return fetch(`/api/v1/discord/users-by-bot/${user}`)
            .then(response => response.json())
            .then(commits => {
                let mediaAvatar = (commits.avatar);
                let mediaName = (commits.username);
                let mediaCard = `
                    <div class="media-card">
                        <div class="media-image">
                            <img src="https://cdn.discordapp.com/avatars/${user}/${mediaAvatar}.webp?size=128" alt="Avatar Media">
                        </div>
                        <div class="media-info">
                            <p class="media-name">${mediaName}</p>
                            <p class="media-description">${medias[user]['description']}</p>
                            <div class="media-socials">
                                ${getSocials(medias[user]['socials'])}
                            </div>
                        </div>
                    </div>
                `
                return mediaCard;
        })
    }

    function getSocials(socials) {
        let socialIcons = "";
        for (let network in socials) {
            if (socials[network]) {
                socialIcons += `<a href="${socials[network]}" target="_blank"><img src="${getSocialIcon(network)}" alt="${network}"></a>`;
            }
        }
        return socialIcons;
    }

    function getSocialIcon(network) {
        switch (network) {
            case 'youtube':
                return '/static/image/youtube.png';
            case 'twitch':
                return '/static/image/twitch.png';
            case 'tiktok':
                return '/static/image/tik-tok.png';
            case 'instagram':
                return '/static/image/instagram.png';
        }
    }

    Promise.all(Object.keys(medias).map(user => setUserCard(user)))
    .then(cards => {
        mediaContainers.innerHTML += cards.join('');
    });
});