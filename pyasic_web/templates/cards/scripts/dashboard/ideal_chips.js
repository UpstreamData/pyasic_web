
// ideal_chips
ideal_chips_card = document.getElementById("card_ideal_chips")
ideal_chips = parseFloat(0)
if (data.hasOwnProperty("miners")) {
    // Dashboard code, multiple miners
    for (i = 0; i< data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("ideal_chips")) {
            ideal_chips += parseFloat(data["miners"][i]["ideal_chips"])
        }
    }
}
if (!!ideal_chips_card) {
    ideal_chips_card.innerHTML = ideal_chips
}
