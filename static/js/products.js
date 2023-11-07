let products = document.getElementsByClassName("products")[0];
let decor = document.getElementsByClassName("decor")[0];

fetch("/api/v1/products")
  .then(response => response.json())
  .then(commits => {
    console.log(commits);
    for (let i = 0; i < Object.keys(commits).length; i++) {
      let itemName=commits[i].name
      let itemPrice=commits[i].price
      let tovar = `
          <div class="card-product">
            <img src="/static/image/tovar.png" alt="" width="150px">
              <h3>${itemName}</h3>
              <h4>${itemPrice}₽</h4>
              <a class="buy" href="#" alt="" onclick="buyProducts()">В корзину</a>
          </div>
              `
      console.log(commits[i])
      products.innerHTML=products.innerHTML+tovar
    }
  });


function buyProducts() {
  console.log("Успешная покупка")
  decor.style.opacity="1";
}