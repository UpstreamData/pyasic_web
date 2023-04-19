// ideal_chips
pct_ideal_chips_card = document.getElementById("card_pct_ideal_chips")
ideal_chips = parseFloat(0)
total_chips = parseFloat(0)
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("ideal_chips")) {
        ideal_chips += parseFloat(i["ideal_chips"])
        total_chips += parseFloat(i["total_chips"])
    }
}
if (ideal_chips > 0) {
    pct_ideal_chips = (Number((total_chips/ideal_chips)*100)).toFixed(2)
} else {
    pct_ideal_chips = 0
}
if (!!pct_ideal_chips_card) {
    pct_ideal_chips_card.innerHTML = pct_ideal_chips + " %"
}
