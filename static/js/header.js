document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector('.header');
    var trash = document.querySelector('.trash-container');
    var image = document.querySelector('.header-items-menu');
    var itemsСontainer = document.querySelector('.header-items-container');
    var firstSection = document.querySelector('section');
    var exitImage = '/static/image/exit.png';
    var menuImage = '/static/image/menu.png';

    function setPadding() {
        firstSection.style.paddingTop = header.offsetHeight + 'px';
        itemsСontainer.style.paddingTop = header.offsetHeight + 'px';
        trash.style.marginTop = header.offsetHeight + 'px';
    }
    setPadding()

    document.querySelector('.header-items-menu').addEventListener('click', function () {
        var fullPath = image.src;
        var imagePath = fullPath.substring(fullPath.lastIndexOf('/static'));

        if (imagePath === menuImage) {
            image.src = exitImage;
            itemsСontainer.style.display = 'flex';
        } else {
            image.src = menuImage;
            itemsСontainer.style.display = 'none';
        }
    });

    window.addEventListener('resize', function () {
        setPadding()
        if (window.innerWidth > 930) {
            image.src = menuImage;
            itemsСontainer.style.display = 'none';
        }
    });
});
