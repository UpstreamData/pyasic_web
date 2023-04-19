// pct_max_wattage
pct_max_wattage_card = document.getElementById("card_pct_max_wattage")
max_wattage = parseFloat(0)
total_wattage = parseFloat(0)
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("wattage_limit")) {
        max_wattage += parseFloat(i["wattage_limit"])
        total_wattage += parseFloat(i["wattage"])
    }
}
if (max_wattage > 0) {
    pct_max_wattage = (Number((wattage/max_wattage)*100)).toFixed(2)
} else {
    pct_max_wattage = 0;
}
if (!!pct_max_wattage_card) {
    pct_max_wattage_card.innerHTML = pct_max_wattage + " %"
}
