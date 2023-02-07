
// pct_ideal_hashrate
pct_ideal_hashrate_card = document.getElementById("card_pct_ideal_hashrate")
pct_ideal_hashrate = parseFloat(0)
if (data.hasOwnProperty("miners")) {
    hashrate = parseFloat(0)
    ideal_hashrate = parseFloat(0)
    // Dashboard code, multiple miners
    for (i = 0; i< data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("hashrate")) {
            ideal_hashrate += parseFloat(data["miners"][i]["nominal_hashrate"])
            hashrate += parseFloat(data["miners"][i]["hashrate"])
        }
    }
    if (ideal_hashrate > 0) {
        pct_ideal_hashrate = (Number((hashrate/ideal_hashrate)*100)).toFixed(2)
    }
}

if (!!pct_ideal_hashrate_card) {
    pct_ideal_hashrate_card.innerHTML = pct_ideal_hashrate + " %"
}
