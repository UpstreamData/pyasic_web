// efficiency
efficiency_card = document.getElementById("card_efficiency")
efficiencyArr = [];
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("efficiency")) {
        efficiencyArr.push(parseFloat(i["efficiency"]))
    }
}
sum = efficiencyArr.reduce((acc, curr) => acc + curr, 0);
efficiency = (Number(sum / efficiencyArr.length)).toFixed(2);
if (isNaN(efficiency)) {
    efficiency = 0
}
if (!!efficiency_card) {
    efficiency_card.innerHTML = efficiency + " J/TH"
}
