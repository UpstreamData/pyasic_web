
// env_temp
env_temp_card = document.getElementById("card_env_temp")
env_temp = parseFloat(0)
if (data.hasOwnProperty("miners")) {
    // Dashboard code, multiple miners
    for (i = 0; i< data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("env_temp")) {
            if (data["miners"][i]["env_temp"] != -1) {
                env_temp += parseFloat(data["miners"][i]["env_temp"])
            }
        }
    }
    env_temp = (Number(env_temp/data["miners"].length)).toFixed(2)
    if (env_temp == 0) {
        env_temp = "?"
    }
}
if (!!env_temp_card) {
    env_temp_card.innerHTML = env_temp + " °C"
}
