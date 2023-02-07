
// pct_max_wattage
pct_max_wattage_card = document.getElementById("card_pct_max_wattage")
pct_max_wattage = parseFloat(0)
if (data.hasOwnProperty("wattage")) {
    // Miner page code, 1 miner
    max_wattage = parseFloat(data["wattage_limit"])
    wattage = parseFloat(data["wattage"])
    pct_max_wattage = (Number((wattage/max_wattage)*100)).toFixed(2)
}
if (!!pct_max_wattage_card) {
    pct_max_wattage_card.innerHTML = pct_max_wattage + " %"
}
