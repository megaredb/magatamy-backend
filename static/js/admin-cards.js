function toggleAnswer(element) {
    // Находим следующий элемент после заголовка (это будет ответ)
    var answer = element.nextElementSibling;

    // Проверяем текущее состояние display и изменяем его
    if (answer.style.display === "none" || answer.style.display === "") {
        answer.style.display = "block";
        answer.style.maxHeight = answer.scrollHeight + "px"; // устанавливаем максимальную высоту для плавного появления
    } else {
        answer.style.display = "none";
        answer.style.maxHeight = null; // убираем максимальную высоту
    }
}
