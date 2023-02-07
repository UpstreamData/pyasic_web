
// hostname
hostname_card = document.getElementById("card_hostname")
hostname = "?"
if (data.hasOwnProperty("hostname")) {
    // Miner page code, 1 miner
    hostname = data["hostname"]
}
if (!!hostname_card) {
    hostname_card.innerHTML = hostname
}
