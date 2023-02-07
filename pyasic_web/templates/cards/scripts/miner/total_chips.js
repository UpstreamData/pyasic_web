
// total_chips
total_chips_card = document.getElementById("card_total_chips")
total_chips = parseFloat(0)
if (data.hasOwnProperty("total_chips")) {
    // Miner page code, 1 miner
    total_chips = parseFloat(data["total_chips"])
}
if (!!total_chips_card) {
    total_chips_card.innerHTML = total_chips
}
