
// hashrate
hashrate_card = document.getElementById("card_hashrate")
hashrate = parseFloat(0)
if (data.hasOwnProperty("miners")) {
    // Dashboard code, multiple miners
    for (i = 0; i< data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("efficiency")) {
            hashrate += parseFloat(data["miners"][i]["hashrate"])
        }
    }
} else if (data.hasOwnProperty("hashrate")) {
    // Miner page code, 1 miner
    hashrate = parseFloat(data["hashrate"])
}
if (hashrate == 0) {
    // no hashrate, measure as TH/s
    hashrate = "0 TH/s"
} else if (hashrate < 1) {
    // Low hashrate, measure as GH/s
    hashrate = parseInt(hashrate*1000) + " GH/s";
} else if (hashrate > 1000) {
    // High hashrate, measure as PH/s
    hashrate = Number((hashrate/1000).toFixed(2)) + " PH/s";
} else {
    // Measure as TH/s
    hashrate = parseInt(hashrate) + " TH/s";
}
if (!!hashrate_card) {
    hashrate_card.innerHTML = hashrate
}
