
// pct_ideal_hashrate
pct_ideal_hashrate_card = document.getElementById("card_pct_ideal_hashrate")
pct_ideal_hashrate = parseFloat(0)
if (data.hasOwnProperty("hashrate")) {
    // Miner page code, 1 miner
    ideal_hashrate = parseFloat(data["nominal_hashrate"])
    hashrate = parseFloat(data["hashrate"])
    pct_ideal_hashrate = (Number((hashrate/ideal_hashrate)*100)).toFixed(2)
}

if (!!pct_ideal_hashrate_card) {
    pct_ideal_hashrate_card.innerHTML = pct_ideal_hashrate + " %"
}
