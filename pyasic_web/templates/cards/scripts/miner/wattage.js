
// wattage
wattage_card = document.getElementById("card_wattage")
wattage = parseFloat(0)
if (data.hasOwnProperty("wattage")) {
    // Miner page code, 1 miner
    wattage = parseFloat(data["wattage"])
}
if (!!wattage_card) {
    wattage_card.innerHTML = wattage + " W"
}
