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
    var trashContainer = document.querySelector('.trash-container');
    var trash = document.querySelector('.trash-image');
    var trashProducts = document.querySelector(".trash-products");
    var button = document.querySelector('.trash-button');

    function setProducts() {
        trashProducts.innerHTML = '';
        return fetch(`/api/v1/products`)
            .then(response => response.json())
            .then(commits => {
                var data = getData();
                var allPrice = 0
                for (var i in commits) {
                    var currentId = commits[i]['id'];
                    if (data.indexOf(currentId) !== -1) {
                        let trashProduct = `
                            <div class="trash-product">
                                <div class="trash-product-top">
                                    <div class="trash-product-images">
                                        <img class="trash-product-image" src="/static/image/${commits[i]['image']}" alt="Product image">
                                        <img class="trash-product-trash" id="${currentId}" src="/static/image/trash-bin.png" alt="Trash image">
                                    </div>
                                    <div class="trash-product-info">
                                        <p>${commits[i]['name']}</p>
                                        <p>цена: ${commits[i]['price']} руб.</p>
                                    </div>
                                    <div class="trash-product-arrow">
                                        <img class="trash-product-arrow-image" src="/static/image/arrow.png" alt="Description">
                                    </div>
                                </div>
                                <div class="trash-product-description">
                                    <p>${commits[i]['description']}</p>
                                </div>
                            </div>
                        `
                        allPrice += commits[i]['price'];
                        button.innerText = `Оплатить ${allPrice} руб.`;
                        trashProducts.innerHTML += trashProduct;
                    }
                }
        })
    }

    document.addEventListener('click', function (event) {
        var trashProductTrash = event.target.closest('.trash-product-trash');

        if (trashProductTrash) {
            var id = parseInt(trashProductTrash.id);
            var data = getData();

            var index = data.indexOf(id);
            if (index !== -1) {
                data.splice(index, 1);

                saveData(data);
                setProducts();
                button.innerText = `Оплатить 0 руб.`;
            }
        }
    });

    trashContainer.addEventListener('click', function (event) {
        if (event.target === trashContainer) {
            trashContainer.style.display = 'none';
        }
    });

    trash.addEventListener('click', function (event) {
        if (trashContainer.style.display === 'none') {
            trashContainer.style.display = 'flex';
            setProducts();
        } else {
            trashContainer.style.display = 'none';
        }
    });

    document.addEventListener('click', function (event) {
        var trashArrowImage = event.target.closest('.trash-product-arrow-image');
        var button = event.target.closest('.trash-button');

        if (trashArrowImage) {
            var trashProduct = trashArrowImage.closest('.trash-product');

            if (trashProduct.style.height !== 'auto') {
                trashProduct.style.height = 'auto';
                trashArrowImage.style.transform = 'rotate(180deg)';
            } else {
                trashProduct.style.height = '100px';
                trashArrowImage.style.transform = 'rotate(0deg)';
            }
        }

        if (button) {
            var data = getData();
            const hasRequestBody = Array.isArray(data) && data.length > 0;

            if (hasRequestBody) {
                const options = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                };

                fetch("/api/v1/payment/payment-url", options)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`Error! Status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (!data.error && data.data.url) {
                            window.open(data.data.url, '_blank');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                });
            }
        }
    });
});
