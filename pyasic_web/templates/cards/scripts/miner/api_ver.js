
// api_ver
api_ver_card = document.getElementById("card_api_ver")
api_ver = "?"
if (data.hasOwnProperty("api_ver")) {
    // Miner page code, 1 miner
    api_ver = data["api_ver"]
}
if (!!api_ver_card) {
    api_ver_card.innerHTML = api_ver
}
