
// pools
pools_card = document.getElementById("card_pools")
pools_card.innerHTML = ""
if (data.hasOwnProperty("pool_1_user")) {
    // Miner page code, 1 miner
    for (let i = 1; i < 3; i++) {
        item = data["pool_" + i + "_user"]
        pools_card.innerHTML += '<div class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + item + '</div>'
    }
}
