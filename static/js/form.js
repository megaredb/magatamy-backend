document.addEventListener("DOMContentLoaded", function () {
    var buttonVanilla = document.querySelector('.button-vanilla');
    var buttonVanillaPlus = document.querySelector('.button-vanilla-plus');

    var form = document.querySelector('.form');
    var formСontainer = document.querySelector('.form-container');

    function setProducts(idForm) {
        return fetch(`/api/v1/tickets/forms/`)
            .then(response => response.json())
            .then(commits => {
                console.log(commits);
                var commit = commits[idForm];
                commit.questions.sort((a, b) => a.position - b.position);
                form.innerHTML = '';
                var forms = '';
                for (var i = 0; i < commit.questions.length; i++) {
                    forms += `
                        <p class="form-question" id="${commit.questions[i].id}" data-question-id="${commit.questions[i].id}">${commit.questions[i].description}</p>
                        <textarea placeholder="Введите текст" id="${commit.questions[i].id}" data-question-id="${commit.questions[i].id}"></textarea>
                    `
                  }

                let formContent = `
                    <div class="form-content">
                        <div class="form-button">
                            <button class="form-button">Отменить</button>
                            <button class="form-button form-button-ok" id="${commit['id']}">Подать заявку</button>
                        </div>
                        <div>
                            ${forms}
                        </div>
                        <h2>${commit['name']}</h2>
                    </div>
                `
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
