document.ready (


    var textArea = document.getElementById("message");
    var remainingChars = document.getElementById("text-remaining");

    var maxChars = 1000;
    textArea.addEventListener("input", () => {
                                    remaining = maxChars - textArea.value.length;
                                    remainingChars.textContent = `$(remaining) chars remaining`;
                                     }
                               )



)

