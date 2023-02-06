
// efficiency
efficiency_card = document.getElementById("card_efficiency")
efficiency = parseFloat(0)
if (data.hasOwnProperty("miners")) {
    // Dashboard code, multiple miners
    for (i = 0; i< data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("efficiency")) {
            efficiency += parseFloat(data["miners"][i]["efficiency"])
        }
    }
    efficiency = (Number(efficiency/data["miners"].length)).toFixed(2)
} else if (data.hasOwnProperty("efficiency")) {
    // Miner page code, 1 miner
    efficiency = parseFloat(data["efficiency"])
}
if (!!efficiency_card) {
    efficiency_card.innerHTML = efficiency + " J/TH"
}
