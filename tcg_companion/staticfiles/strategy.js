function generateStrategy() {
    const form = document.getElementById("strategy-form");
    const box = document.getElementById("strategy-box");
    const text = document.getElementById("strategy-text");

    if (form) {
        form.addEventListener("submit", e => {
            e.preventDefault();

            fetch(form.action || window.location.href, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            })
                .then(response => response.json())
                .then(data => {
                    if (data.strategy) {
                        text.innerText = data.strategy;
                        box.style.display = "block";
                    } else if (data.error) {
                        text.innerText = "Error: " + data.error;
                        box.style.display = "block";
                    }
                })
                .catch(error => {
                    text.innerText = "Network error: " + error;
                    box.style.display = "block";
                });
        });
    }
};
