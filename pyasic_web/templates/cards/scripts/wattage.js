
// wattage
wattage_card = document.getElementById("card_wattage")
wattage = parseFloat(0)
if (data.hasOwnProperty("miners")) {
    // Dashboard code, multiple miners
    for (i = 0; i< data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("wattage")) {
            wattage += parseFloat(data["miners"][i]["wattage"])
        }
    }
} else if (data.hasOwnProperty("wattage")) {
    // Miner page code, 1 miner
    wattage = parseFloat(data["wattage"])
}
if (!!wattage_card) {
    wattage_card.innerHTML = wattage + " J/TH"
}
