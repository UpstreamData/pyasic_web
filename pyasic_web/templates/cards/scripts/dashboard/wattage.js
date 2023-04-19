// wattage
wattage_card = document.getElementById("card_wattage")
wattage = parseFloat(0)
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("wattage")) {
        wattage += parseFloat(i["wattage"])
    }
}
if (!!wattage_card) {
    wattage_card.innerHTML = wattage
}
