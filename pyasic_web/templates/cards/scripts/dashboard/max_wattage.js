
// max_wattage
max_wattage_card = document.getElementById("card_max_wattage")
max_wattage = parseFloat(0)
if (data.hasOwnProperty("miners")) {
    // Dashboard code, multiple miners
    for (i = 0; i< data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("wattage_limit")) {
            max_wattage += parseFloat(data["miners"][i]["wattage_limit"])
        }
    }
}
if (!!max_wattage_card) {
    max_wattage_card.innerHTML = max_wattage + " J/TH"
}
