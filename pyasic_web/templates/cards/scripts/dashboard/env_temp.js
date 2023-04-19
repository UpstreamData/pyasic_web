// env_temp
env_temp_card = document.getElementById("card_env_temp")
env_tempArr = [];
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("env_temp")) {
        env_tempArr.push(parseFloat(i["env_temp"]))
    }
}
sum = env_tempArr.reduce((acc, curr) => acc + curr, 0);
env_temp = (Number(sum / env_tempArr.length)).toFixed(2);
if (isNaN(env_temp)) {
    env_temp = 0
}
if (env_temp == -1) {
    env_temp = 0
}
if (!!env_temp_card) {
    env_temp_card.innerHTML = env_temp + " °C"
}
