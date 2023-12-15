function saveData(data) {
  var jsonString = JSON.stringify(data);

  localStorage.setItem('myData', jsonString);
}

function getData() {
  var jsonString = localStorage.getItem('myData');
  var data = JSON.parse(jsonString);

  return data;
}

document.addEventListener("DOMContentLoaded", function () {
    var productsContainer = document.querySelector(".products-container");
    var trashImage = document.querySelector(".trash-image");

    function setProducts(user) {
        return fetch(`/api/v1/products`)
            .then(response => response.json())
            .then(commits => {
                for (var i in commits) {
                    let productСontainer = `
                        <div class="product-container">
                            <div class="product-image">
                                <img src="/static/image/test.png" alt="Product image">
                            </div>
                            <p>${commits[i]['name']}</p>
                            <button class="product-button" id="${commits[i]['id']}">Купить за ${commits[i]['price']}</button>
                        </div>
                    `
                    productsContainer.innerHTML += productСontainer;
                }
        })
    }
    setProducts();

    productsContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('product-button')) {
            var id = +event.target.id;
            var data = getData() || [];

            if (!data.includes(id)) {
                data.push(id);

                saveData(data);

                trashImage.setAttribute('id', 'pulseEffect');
                setTimeout(() => {
                    trashImage.removeAttribute('id');
                }, 200);
            }
        }
    });
});