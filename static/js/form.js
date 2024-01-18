document.addEventListener("DOMContentLoaded", function () {
    var buttonVanilla = document.querySelector('.button-vanilla');
    var buttonVanillaPlus = document.querySelector('.button-vanilla-plus');

    var form = document.querySelector('.form');
    var formСontainer = document.querySelector('.form-container');

    function setProducts(idForm) {
        return fetch(`/api/v1/tickets/forms/`)
            .then(response => response.json())
            .then(commits => {
                form.innerHTML = '';
                let formContent = '';
                if (!commits.detail)
                {
                    var commit = commits[idForm];

                    var purchasable = commit['purchasable'];
                    var has_access = commit['has_access'];

                    if (purchasable && !has_access)
                    {
                        formContent = `
                            <div class="form-content">
                                <div class="form-button">
                                    <button class="form-button">Отменить</button>
                                    <button class="form-button">ОК</button>
                                </div>
                                <p style="text-align: center; padding-bottom: 16px; color: red;">У вас не приобретен товар!</p>
                                <h2>${commit['name']}</h2>
                            </div>
                        `
                    }
                    else
                    {
                        commit.questions.sort((a, b) => a.position - b.position);
                        var forms = '';
                        for (var i = 0; i < commit.questions.length; i++) {
                            forms += `
                                <p class="form-question" id="${commit.questions[i].id}" data-question-id="${commit.questions[i].id}">${commit.questions[i].description}</p>
                                <textarea placeholder="Введите текст" id="${commit.questions[i].id}" data-question-id="${commit.questions[i].id}"></textarea>
                            `
                          }

                        formContent = `
                            <div class="form-content">
                                <div class="form-button">
                                    <button class="form-button">Отменить</button>
                                    <button class="form-button form-button-ok" id="${commit['id']}">Подать заявку</button>
                                </div>
                                <div>
                                    ${forms}
                                    <p style="padding-bottom: 16px;">Отправляя данную форму вы соглашаетесь с нашим соглашением и  политикой конфиденциальности!</p>
                                </div>
                                <h2>${commit['name']}</h2>
                            </div>
                        `
                    }
                }
                else
                {
                    formContent = `
                        <div class="form-content">
                            <div class="form-button">
                                <button class="form-button">Отменить</button>
                                <button class="form-button">ОК</button>
                            </div>
                            <p style="text-align: center; padding-bottom: 16px; color: red;">Вы не вошли в Discord!</p>
                        </div>
                    `
                }
                form.innerHTML += formContent;
        })
    }

    buttonVanilla.addEventListener('click', function () {
        setProducts(0)
        formСontainer.style.display = 'flex';
    });

    buttonVanillaPlus.addEventListener('click', function () {
        setProducts(1)
        formСontainer.style.display = 'flex';
    });

    formСontainer.addEventListener('click', function (event) {
        if ((event.target === formСontainer) || (event.target.classList.contains('form-button'))) {
            formСontainer.style.display = 'none';
        }
    });

    document.addEventListener('click', function (event) {
        var buttonOk = document.querySelector('.form-button-ok');

        if (event.target === buttonOk) {
            var formId = buttonOk.id;

            var formQuestions = document.querySelectorAll('.form-question');

            var answers = [];

            formQuestions.forEach(function (element) {
                var questionId = element.getAttribute('data-question-id');
                var textValue;

                var textareaElement = document.querySelector(`textarea[data-question-id="${questionId}"]`);
                if (textareaElement) {
                    textValue = textareaElement.value;
                } else {
                    textValue = element.textContent;
                }

                answers.push({
                    question_id: questionId,
                    text_value: textValue,
                    bool_value: true
                });
            });


            var postData = {
                form_id: formId,
                answers: answers
            };

            fetch('/api/v1/tickets', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(postData)
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.detail);
            });
        }
    });
});
