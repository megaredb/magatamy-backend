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
        "1112736860221997076": {
            "description": "",
            "socials": {    
                "youtube": "https://www.youtube.com/@gromlastday"
            }
        },
        "1114198957581664306": {
            "description": "",
            "socials": {
                "youtube": "https://www.youtube.com/@Spa_wnMAGATAMY"
            }
        },
        "763837225199861772": {
            "description": "Просто верный Джо",
            "socials": {
                "youtube": "https://www.youtube.com/@The-Joseph"
            }
        },
        "269542487998201857": {
            "description": "",
            "socials": {
                "youtube": "https://youtube.com/@AGK_Nagibeter"
            }
        },
        "573080435102449664": {
            "description": "",
            "socials": {
                "youtube": "https://youtube.com/@ender105"
            }
        },
        "1124958266015887421": {
            "description": "",
            "socials": {
                "youtube": "https://www.youtube.com/@frankostvol"
            }
        },
        "1037288672418091038": {
            "description": "",
            "socials": {
                "youtube": "https://www.youtube.com/@HorusChannelYT"
            }
        },
        "1069937338026827796": {
            "description": "",
            "socials": {
                "youtube": "https://www.youtube.com/@Nirte4ek_Minecraft"
            }
        },
        "705315583323013182": {
            "description": "",
            "socials": {
                "youtube": "https://www.youtube.com/@Chokopick"
            }
        },
        "946370462793990214": {
            "description": "",
            "socials": {
                "youtube": "https://www.youtube.com/@cherepok_03"
            }
        }
    };

    function setUserCard(user) {
        return fetch(`/api/v1/discord/users-by-bot/${user}`)
            .then(response => response.json())
            .then(commits => {
                let mediaAvatar = (commits.avatar);
                let mediaName = (commits.nick);
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