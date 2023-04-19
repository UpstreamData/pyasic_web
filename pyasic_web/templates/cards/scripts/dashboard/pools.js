// pools
pools_card = document.getElementById("card_pools")
pools_card.innerHTML = ""
const poolUsers = {};
for (const item of Object.values(data)) {
  if (item.hasOwnProperty("pool_1_user")) {
    const username = item["pool_1_user"];
    poolUsers[username] = poolUsers.hasOwnProperty(username) ? poolUsers[username] + 1 : 1;
  }
}
// Dashboard code, multiple miners
for (item in poolUsers) {
    pools_card.innerHTML += '<div class ="list-group-item d-flex justify-content-between">' + item + '<span class="badge bg-fancy-gradient rounded-pill align-items-middle p-2 m-0" style="width:50px;">' + poolUsers[item] + '</span></div>'
};
