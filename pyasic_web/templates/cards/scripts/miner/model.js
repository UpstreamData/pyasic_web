
// model
model_card = document.getElementById("card_model")
model = "?"
if (data.hasOwnProperty("model")) {
    // Miner page code, 1 miner
    model = data["model"]
}
if (!!model_card) {
    model_card.innerHTML = model
}
