
// temperature_avg
temperature_avg_card = document.getElementById("card_avg_temperature")
temperature_avg = parseFloat(0)
if (data.hasOwnProperty("temperature_avg")) {
    // Miner page code, 1 miner
    temperature_avg = parseFloat(data["temperature_avg"])
}
if (!!temperature_avg_card) {
    temperature_avg_card.innerHTML = temperature_avg + "  °C"
}
