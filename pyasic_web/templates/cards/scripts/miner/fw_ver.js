
// fw_ver
fw_ver_card = document.getElementById("card_fw_ver")
fw_ver = "?"
if (data.hasOwnProperty("fw_ver")) {
    // Miner page code, 1 miner
    fw_ver = data["fw_ver"]
}
if (!!fw_ver_card) {
    fw_ver_card.innerHTML = fw_ver
}
