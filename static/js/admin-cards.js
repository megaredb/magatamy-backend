function toggleAnswer(element) {
    var answer = element.nextElementSibling;

    if (answer.style.display === "none" || answer.style.display === "")
    {
        answer.style.display = "block";
        answer.style.maxHeight = answer.scrollHeight + "px";
    }
    else
    {
        answer.style.display = "none";
        answer.style.maxHeight = null;
    }
}
