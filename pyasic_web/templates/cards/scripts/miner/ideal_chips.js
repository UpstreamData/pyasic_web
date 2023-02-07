
// ideal_chips
ideal_chips_card = document.getElementById("card_ideal_chips")
ideal_chips = parseFloat(0)
if (data.hasOwnProperty("ideal_chips")) {
    // Miner page code, 1 miner
    ideal_chips = parseFloat(data["ideal_chips"])
}
if (!!ideal_chips_card) {
    ideal_chips_card.innerHTML = ideal_chips
}
