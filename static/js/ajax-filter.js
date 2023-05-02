function ajaxSend(url, params) {
    // Отправляем запрос
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => render(json))
        .catch(error => console.error(error))
}

// Filter movies
// const forms = document.querySelector('form[name=filter]');

// forms.addEventListener('submit', function (e) {
//     // Получаем данные из формы
//     e.preventDefault(); // убираем настройки по умолчанию
//     let url = this.action;
//     let params = new URLSearchParams(new FormData(this)).toString(); // сюда поступают данные с формы
//     ajaxSend(url, params);
// });


function render(data) {
    // Рендер шаблона
    let template_list = Hogan.compile(html_list);
    let template_grid = Hogan.compile(html_grid)
    let output_list = template_list.render(data);
    let output_grid = template_grid.render(data);

    const div_list = document.querySelector('.wrapper>.main-shop-page>.container>.row>.col-lg-9>.main-categorie>.tab-content>#list-view');
    const div_grid = document.querySelector('.wrapper>.main-shop-page>.container>.row>.col-lg-9>.main-categorie>.tab-content>#grid-view>.row');
    div_list.innerHTML = output_list;
    div_grid.innerHTML = output_grid;
}

let html_list = '\
{{#products}}\
<div class="single-product">\
    <!-- Product Image Start -->\
    <div class="pro-img">\
        <a href="{{ slug }}">\
            <img class="primary-img" src="/media/{{ photos__photo }}" alt="single-product" width="270px" height="210px">\
        </a>\
    </div>\
    <!-- Product Image End -->\
    <!-- Product Content Start -->\
    <div class="pro-content">\
        <div class="product-rating">\
            <i class="fa fa-star"></i>\
            <i class="fa fa-star"></i>\
            <i class="fa fa-star"></i>\
            <i class="fa fa-star"></i>\
            <i class="fa fa-star"></i>\
        </div>\
        <h4><a href="{{ slug }}">{{ name }}</a></h4>\
        <p><span class="price">{{ cost }} руб.</span><del class="prev-price"></del></p>\
        <p>{{ description }}</p>\
        <div class="pro-actions">\
            <div class="actions-secondary">\
                <a href="wishlist.html" data-toggle="tooltip" title="Add to Wishlist"><i class="fa fa-heart"></i></a>\
                <a class="add-cart" href="cart.html" data-toggle="tooltip" title="Add to Cart">Add To Cart</a>\
                <a href="compare.html" data-toggle="tooltip" title="Add to Compare"><i class="fa fa-signal"></i></a>\
            </div>\
        </div>\
    </div>\
    <!-- Product Content End -->\
</div>\
{{/products}}'

let html_grid = '\
{{#products}}\
<div class="col-lg-4 col-sm-6">\
    <div class="single-product">\
        <!-- Product Image Start -->\
        <div class="pro-img">\
            <a href="{{ slug }}">\
                <img class="primary-img" src="/media/{{ photos__photo }}" alt="single-product" width="270px" height="210px">\
            </a>\
        </div>\
        <!-- Product Image End -->\
        <!-- Product Content Start -->\
        <div class="pro-content">\
            <div class="product-rating">\
                <i class="fa fa-star"></i>\
                <i class="fa fa-star"></i>\
                <i class="fa fa-star"></i>\
                <i class="fa fa-star"></i>\
                <i class="fa fa-star"></i>\
            </div>\
            <h4><a href="{{ slug }}">{{ name }}</a></h4>\
            <p><span class="price">{{ cost }} руб.</span><del class="prev-price"></del></p>\
            <div class="pro-actions">\
                <div class="actions-secondary">\
                    <a href="wishlist.html" data-toggle="tooltip" title="Add to Wishlist"><i class="fa fa-heart"></i></a>\
                    <a class="add-cart" href="cart.html" data-toggle="tooltip" title="Add to Cart">Add To Cart</a>\
                    <a href="compare.html" data-toggle="tooltip" title="Add to Compare"><i class="fa fa-signal"></i></a>\
                </div>\
            </div>\
        </div>\
        <!-- Product Content End -->\
    </div>\
</div>\
{{/products}}'

// Add star rating
// const rating = document.querySelector('form[name=rating]');

// rating.addEventListener("change", function (e) {
//     // Получаем данные из формы
//     let data = new FormData(this);
//     fetch(`${this.action}`, {
//         method: 'POST',
//         body: data
//     })
//         .then(response => alert("Рейтинг установлен"))
//         .catch(error => alert("Ошибка"))
// });