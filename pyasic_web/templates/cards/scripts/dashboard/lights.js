// lights
lights_on_card = document.getElementById("card_lights_on")
lights_off_card = document.getElementById("card_lights_off")
lights_on_card.innerHTML = ""
lights_off_card.innerHTML = ""
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("fault_light")) {
        if (i["fault_light"]) {
            lights_on_card.innerHTML += '<div class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + i["ip"] + '</div>'
        } else {
            lights_off_card.innerHTML += '<div class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + i["ip"] + '</div>'
        }
    }
}
