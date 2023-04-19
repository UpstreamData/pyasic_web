// ideal_hashrate
pct_ideal_hashrate_card = document.getElementById("card_pct_ideal_hashrate")
ideal_hashrate = parseFloat(0)
total_hashrate = parseFloat(0)
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("hashrate")) {
        ideal_hashrate += parseFloat(i["nominal_hashrate"]);
        total_hashrate += parseFloat(i["hashrate"]);
    }
}
if (ideal_hashrate > 0) {
    pct_ideal_hashrate = (Number((total_hashrate/ideal_hashrate)*100)).toFixed(2);
} else {
    pct_ideal_hashrate = 0;
}
if (!!pct_ideal_hashrate_card) {
    pct_ideal_hashrate_card.innerHTML = pct_ideal_hashrate + " %"
}
