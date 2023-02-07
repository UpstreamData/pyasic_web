
// ideal_hashrate
ideal_hashrate_card = document.getElementById("card_ideal_hashrate")
ideal_hashrate = parseFloat(0)
if (data.hasOwnProperty("nominal_hashrate")) {
    // Miner page code, 1 miner
    ideal_hashrate = parseFloat(data["nominal_hashrate"])
}
if (ideal_hashrate == 0) {
    // no ideal hashrate, measure as TH/s
    ideal_hashrate = "0 TH/s"
} else if (ideal_hashrate < 1) {
    // Low ideal hashrate, measure as GH/s
    ideal_hashrate = parseInt(ideal_hashrate*1000) + " GH/s";
} else if (ideal_hashrate > 1000) {
    // High ideal hashrate, measure as PH/s
    ideal_hashrate = Number((ideal_hashrate/1000).toFixed(2)) + " PH/s";
} else {
    // Measure as TH/s
    ideal_hashrate = parseInt(ideal_hashrate) + " TH/s";
}
if (!!ideal_hashrate_card) {
    ideal_hashrate_card.innerHTML = ideal_hashrate
}
