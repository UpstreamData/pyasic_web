
// temperature_avg
temperature_avg_card = document.getElementById("card_avg_temperature")
temperature_avg = parseFloat(0)
if (data.hasOwnProperty("miners")) {
    // Dashboard code, multiple miners
    for (i = 0; i< data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("temperature_avg")) {
            temperature_avg += parseFloat(data["miners"][i]["temperature_avg"])
        }
    }
    temperature_avg = (Number(temperature_avg/data["miners"].length)).toFixed(2)
}
if (!!temperature_avg_card) {
    temperature_avg_card.innerHTML = temperature_avg + " °C"
}
