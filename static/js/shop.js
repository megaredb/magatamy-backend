document.addEventListener("DOMContentLoaded", function () {
    var productsContainer = document.querySelector(".products-container");

    function setProducts(user) {
        return fetch(`/api/v1/products`)
            .then(response => response.json())
            .then(commits => {
                for (var i in commits) {
                    let productСontainer = `
                        <div class="product-container">
                            <div class="product-image">
                                <img src="/static/image/test.png" alt="Product">
                            </div>
                            <p>${commits[i]['name']}</p>
                            <button>Купить за ${commits[i]['price']}</button>
                        </div>
                    `
                    productsContainer.innerHTML += productСontainer
                }
        })
    }
    setProducts();
});