document.addEventListener("DOMContentLoaded", function () {
    var buttonVanilla = document.querySelector('.button-vanilla');
    var buttonVanillaPlus = document.querySelector('.button-vanilla-plus');

    var form = document.querySelector('.form');
    var formСontainer = document.querySelector('.form-container');

    var dataTest1 = {
        "id": 0,
        "title": "Заявка на Magatamy vanilla",
        "form": ["Ник", "Что-то еще", "Сколько храмасом", "Как дела?", "Ну и для теста"]
    }

    var dataTest2 = {
        "id": 1,
        "title": "Заявка на Magatamy vanilla+",
        "form": ["Ник", "Что-то еще"]
    }

    function setProducts(data) {
        form.innerHTML = '';
        var forms = ''
        for (var i = 0; i < data.form.length; i++) {
            forms += `
                <p>${data['form'][i]}</p>
                <textarea placeholder="Введите текст"></textarea>
            `
          }

        let formContent = `
            <div class="form-content">
                <div class="form-button">
                    <button class="form-button">Отменить</button>
                    <button class="form-button" id="${data['id']}">Подать заявку</button>
                </div>
                <div>
                    ${forms}
                </div>
                <h2>${data['title']}</h2>
            </div>
        `
        form.innerHTML += formContent;
    }

    buttonVanilla.addEventListener('click', function () {
        setProducts(dataTest1)
        formСontainer.style.display = 'flex';
    });

    buttonVanillaPlus.addEventListener('click', function () {
        setProducts(dataTest2)
        formСontainer.style.display = 'flex';
    });

    formСontainer.addEventListener('click', function (event) {
        if ((event.target === formСontainer) || (event.target.classList.contains('form-button'))) {
            formСontainer.style.display = 'none';
        }
    });
});
