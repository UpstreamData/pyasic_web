
// max_wattage
max_wattage_card = document.getElementById("card_max_wattage")
max_wattage = parseFloat(0)
if (data.hasOwnProperty("wattage_limit")) {
    // Miner page code, 1 miner
    max_wattage = parseFloat(data["wattage_limit"])
}
if (!!max_wattage_card) {
    max_wattage_card.innerHTML = max_wattage + " W"
}
