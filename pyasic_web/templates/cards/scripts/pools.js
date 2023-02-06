
// pools
pools_card = document.getElementById("card_pools")
pools_card.innerHTML = ""
if (data.hasOwnProperty("pool_users")) {
    // Dashboard code, multiple miners
    for (item in data["pool_users"]) {
        pools_card.innerHTML += '<div class ="list-group-item d-flex justify-content-between">' + item + '<span class="badge bg-gradient rounded-pill alight-items-middle p-2 m-0" style="width:50px;">' + data["pool_users"][item] + '</span></div>'
    };
} else {
    // Miner page code, 1 miner
    for (let i = 1; i < 3; i++) {
        item = data["pool_" + i + "_user"]
        pools_card.innerHTML += '<div class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + item + '</div>'
    }
}
