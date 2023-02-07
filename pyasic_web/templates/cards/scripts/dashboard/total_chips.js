
// total_chips
total_chips_card = document.getElementById("card_total_chips")
total_chips = parseFloat(0)
if (data.hasOwnProperty("miners")) {
    // Dashboard code, multiple miners
    for (i = 0; i< data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("total_chips")) {
            total_chips += parseFloat(data["miners"][i]["total_chips"])
        }
    }
}
if (!!total_chips_card) {
    total_chips_card.innerHTML = total_chips
}
