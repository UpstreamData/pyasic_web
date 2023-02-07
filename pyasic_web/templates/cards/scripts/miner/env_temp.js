
// env_temp
env_temp_card = document.getElementById("card_env_temp")
env_temp = parseFloat(0)
if (data.hasOwnProperty("env_temp")) {
    // Miner page code, 1 miner
    env_temp = parseFloat(data["env_temp"])
    if (env_temp == -1) {
        env_temp = "?"
    }
}
if (!!env_temp_card) {
    env_temp_card.innerHTML = env_temp + " °C"
}
