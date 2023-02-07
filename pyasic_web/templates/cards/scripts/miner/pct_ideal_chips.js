
// pct_ideal_chips
pct_ideal_chips_card = document.getElementById("card_pct_ideal_chips")
pct_ideal_chips = parseFloat(0)
if (data.hasOwnProperty("total_chips")) {
    // Miner page code, 1 miner
    ideal_chips = parseFloat(data["ideal_chips"])
    total_chips = parseFloat(data["total_chips"])
    if (ideal_chips > 0) {
        pct_ideal_chips = (Number((total_chips/ideal_chips)*100)).toFixed(2)
    }
}

if (!!pct_ideal_chips_card) {
    pct_ideal_chips_card.innerHTML = pct_ideal_chips + " %"
}
