
// make
make_card = document.getElementById("card_make")
make = "?"
if (data.hasOwnProperty("make")) {
    // Miner page code, 1 miner
    make = data["make"]
}
if (!!make_card) {
    make_card.innerHTML = make
}
