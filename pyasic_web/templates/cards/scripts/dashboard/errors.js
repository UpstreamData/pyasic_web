
// errors
errors_card = document.getElementById("card_errors")
errors = ""
// Dashboard code, multiple miners
for (const i of Object.values(data)) {
    if (i.hasOwnProperty("errors")) {
        if (i["errors"].length > 0) {
            miner_id_local = i["ip"].replaceAll(".", "-")
            err_loc = document.getElementById("errors_" + miner_id_local)
            if (err_loc) {
                if (err_loc.classList.contains('show')) {
                    miner_errs_local_html = '<a data-bs-toggle="collapse" href="#errors_' + miner_id_local + '" role="button" class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error" aria-expanded="true">' + i["ip"] + '<span class="badge bg-fancy-gradient rounded-pill alight-items-middle p-2 m-0" style="width:50px;">' + i["errors"].length + '</span></a>'
                    miner_errs_local_html += '<div class="collapse no-transition multi-collapse my-0 py-0 ms-5 show" id="errors_' + miner_id_local + '">'
                    for (err in i["errors"]) {
                        miner_errs_local_html += '<div class ="list-group-item no-transition miner-error-item">' + i["errors"][err]["error_message"] + '</div>'
                    };
                    miner_errs_local_html += '</div>'
                } else {
                    miner_errs_local_html = '<a data-bs-toggle="collapse" href="#errors_' + miner_id_local + '" role="button" class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + i["ip"] + '<span class="badge bg-fancy-gradient rounded-pill alight-items-middle p-2 m-0" style="width:50px;">' + i["errors"].length + '</span></a>'
                    miner_errs_local_html += '<div class="collapse no-transition multi-collapse my-0 py-0 ms-5" id="errors_' + miner_id_local + '">'
                    for (err in i["errors"]) {
                        miner_errs_local_html += '<div class ="list-group-item no-transition miner-error-item">' + i["errors"][err]["error_message"] + '</div>'
                    };
                    miner_errs_local_html += '</div>'
                }
            } else {
                miner_errs_local_html = '<a data-bs-toggle="collapse" href="#errors_' + miner_id_local + '" role="button" class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + i["ip"] + '<span class="badge bg-fancy-gradient rounded-pill alight-items-middle p-2 m-0" style="width:50px;">' + i["errors"].length + '</span></a>'
                miner_errs_local_html += '<div class="collapse no-transition multi-collapse my-0 py-0 ms-5" id="errors_' + miner_id_local + '">'
                for (err in i["errors"]) {
                    miner_errs_local_html += '<div class ="list-group-item no-transition miner-error-item">' + i["errors"][err]["error_message"] + '</div>'
                };
                miner_errs_local_html += '</div>'
            }
            errors += miner_errs_local_html
        }
    };
}
if (!!errors_card) {
    errors_card.innerHTML = errors
}
