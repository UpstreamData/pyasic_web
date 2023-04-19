// max_wattage
max_wattage_card = document.getElementById("card_max_wattage")
max_wattage = parseFloat(0)
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("wattage_limit")) {
        max_wattage += parseFloat(i["wattage_limit"])
    }
}
if (!!max_wattage_card) {
    max_wattage_card.innerHTML = max_wattage + " W"
}
