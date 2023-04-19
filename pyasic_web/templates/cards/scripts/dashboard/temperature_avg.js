// temperature_avg
temperature_avg_card = document.getElementById("card_avg_temperature")
temperature_avgArr = [];
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("temperature_avg")) {
        temperature_avgArr.push(parseFloat(i["temperature_avg"]))
    }
}
sum = temperature_avgArr.reduce((acc, curr) => acc + curr, 0);
temperature_avg = (Number(sum / temperature_avgArr.length)).toFixed(2);
if (isNaN(temperature_avg)) {
    temperature_avg = 0
}
if (!!temperature_avg_card) {
    temperature_avg_card.innerHTML = temperature_avg + " °C"
}
