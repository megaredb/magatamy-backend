document.addEventListener("DOMContentLoaded", function () {
    var requestContainer = document.querySelector(".request-container");
    var forms;

    function setForms() {
        return fetch(`/api/v1/tickets/forms/?skip=0&limit=100`)
            .then(response => response.json())
            .then(commits => {
                  forms = commits;

                  setRequests()
                  setInterval(setRequests, 2000);
        })
    }

    function setRequests() {
        return fetch(`/api/v1/tickets/?ticket_status=0&skip=0&limit=100`)
            .then(response => response.json())
            .then(commits => {
                requestContainer.innerHTML = ''
                for (var i in commits) {
                    var id = commits[i]['id'];
                    var formId = commits[i]['form_id'];
                    var memberId = commits[i]['member_id'];
                    var answersAll = commits[i]['answers'];
                    var answers = '';

                    for (var i = 0; i < forms.length; i++)
                    {
                        if (forms[i]['id'] === formId)
                        {
                            var server = forms[i]['name'];
                            var formAnswers = forms[i]['questions'];
                        }
                    }

                    var imgSrc = (formId === 2) ? "static/image/vanilla.png" : "static/image/vanilla-plus.png";

                    for (var i = 0; i < answersAll.length; i++) {
                        if (formAnswers[i]['title'] === "Ник") var username = answersAll[i]['text_value'];
                        answers += `
                            <div class="question-item">
                                <h3 onclick="toggleAnswer(this)">${formAnswers[i]['description']}</h3>
                                <p>${answersAll[i]['text_value']}</p>
                            </div>
                        `
                     }

                    let requestHTML = `
                        <div class="request">
                            <div class="ava-img">
                                <img src="${imgSrc}" alt="Server image">
                                <div class="buttons">
                                    <a href="#"><button class="request-button-v ${formId}-${username}" id="${id}">V</button></a>
                                    <a href="#"><button class="request-button-x" id="${id}">X</button></a>
                                </div>
                            </div>
                            <div class="right-container">
                                <div class="top">
                                    <h1>${server}</h1>
                                </div>
                                <div class="text">
                                    <div class ="text-colum-left">
                                        ${answers}
                                    </div>
                                </div>
                            </div>
                        </div>
                    `
                    requestContainer.innerHTML += requestHTML;
                }
        })
    }

    function addWhitelist(server, username) {
        return fetch(`/api/v1/minecraft/${server}/whitelist/${username}`)
            .then(response => response.json())
            .then(commits => {})
    }

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('request-button-v')) {
            var data = event.target.classList[1].split("-");
            var server = (data[0] == 2) ? "vanilla" : "vanilla-plus";
            var username = data[1];

            var postData = {
                status: 2
            };

            fetch(`/api/v1/tickets/${event.target.id}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(postData)
            })
            .then(response => response.json())
            .then(data => {
                setRequests();
                addWhitelist(server, username);
            });
        }

        if (event.target.classList.contains('request-button-x')) {
            var postData = {
                status: 1
            };

            fetch(`/api/v1/tickets/${event.target.id}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(postData)
            })
            .then(response => response.json())
            .then(data => {
                setRequests();
            });
        }
    });

    setForms();
});