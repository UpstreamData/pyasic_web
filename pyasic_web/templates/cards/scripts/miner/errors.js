
// errors
errors_card = document.getElementById("card_errors")
errors = ""
if (data.hasOwnProperty("errors")) {
    // Miner page code, 1 miner
        for (i = 0; i < data["errors"].length; i++) {
            errors += '<div class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + data["errors"][i]["error_message"] + '</div>'
        };
}
if (!!errors_card) {
    errors_card.innerHTML = errors
}
