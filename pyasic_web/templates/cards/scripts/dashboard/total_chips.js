// total_chips
total_chips_card = document.getElementById("card_total_chips")
total_chips = parseFloat(0)
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("total_chips")) {
        total_chips += parseFloat(i["total_chips"])
    }
}
if (!!total_chips_card) {
    total_chips_card.innerHTML = total_chips
}
