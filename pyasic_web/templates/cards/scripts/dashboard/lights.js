
// lights
lights_on_card = document.getElementById("card_lights_on")
lights_off_card = document.getElementById("card_lights_off")
lights_on_card.innerHTML = ""
lights_off_card.innerHTML = ""
if (data.hasOwnProperty("miners")) {
    // Dashboard code, multiple miners
    for (i = 0; i < data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("fault_light")) {
            if (data["miners"][i]["fault_light"]) {
                lights_on_card.innerHTML += '<div class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + data["miners"][i]["ip"] + '</div>'
            } else {
                lights_off_card.innerHTML += '<div class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + data["miners"][i]["ip"] + '</div>'
            }
        }
    }
}
