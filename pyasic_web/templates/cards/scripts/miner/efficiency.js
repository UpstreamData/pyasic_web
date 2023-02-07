
// efficiency
efficiency_card = document.getElementById("card_efficiency")
efficiency = parseFloat(0)
if (data.hasOwnProperty("efficiency")) {
    // Miner page code, 1 miner
    efficiency = parseFloat(data["efficiency"])
}
if (!!efficiency_card) {
    efficiency_card.innerHTML = efficiency + " J/TH"
}
