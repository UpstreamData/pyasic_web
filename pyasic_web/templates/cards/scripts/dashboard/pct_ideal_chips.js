
// pct_ideal_chips
pct_ideal_chips_card = document.getElementById("card_pct_ideal_chips")
pct_ideal_chips = parseFloat(0)
if (data.hasOwnProperty("miners")) {
    chips = parseFloat(0)
    ideal_chips = parseFloat(0)
    // Dashboard code, multiple miners
    for (i = 0; i< data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("total_chips")) {
            ideal_chips += parseFloat(data["miners"][i]["ideal_chips"])
            chips += parseFloat(data["miners"][i]["total_chips"])
        }
    }
    if (ideal_chips > 0) {
        pct_ideal_chips = (Number((chips/ideal_chips)*100)).toFixed(2)
    }
}

if (!!pct_ideal_chips_card) {
    pct_ideal_chips_card.innerHTML = pct_ideal_chips + " %"
}
