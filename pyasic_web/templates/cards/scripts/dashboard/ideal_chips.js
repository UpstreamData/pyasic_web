// ideal_chips
ideal_chips_card = document.getElementById("card_ideal_chips")
ideal_chips = parseFloat(0)
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("ideal_chips")) {
        ideal_chips += parseFloat(i["ideal_chips"])
    }
}
if (!!ideal_chips_card) {
    ideal_chips_card.innerHTML = ideal_chips
}
