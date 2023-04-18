
// errors
errors_card = document.getElementById("card_errors")
errors = ""
if (data.hasOwnProperty("miners")) {
    // Dashboard code, multiple miners
    for (i = 0; i < data["miners"].length; i++) {
        if (data["miners"][i].hasOwnProperty("errors")) {
            if (data["miners"][i]["errors"].length > 0) {
                miner_id_local = data["miners"][i]["ip"].replaceAll(".", "-")
                err_loc = document.getElementById("errors_" + miner_id_local)
                if (err_loc) {
                    if (err_loc.classList.contains('show')) {
                        miner_errs_local_html = '<a data-bs-toggle="collapse" href="#errors_' + miner_id_local + '" role="button" class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error" aria-expanded="true">' + data["miners"][i]["ip"] + '<span class="badge bg-fancy-gradient rounded-pill alight-items-middle p-2 m-0" style="width:50px;">' + data["miners"][i]["errors"].length + '</span></a>'
                        miner_errs_local_html += '<div class="collapse no-transition multi-collapse my-0 py-0 ms-5 show" id="errors_' + miner_id_local + '">'
                        for (err in data["miners"][i]["errors"]) {
                            miner_errs_local_html += '<div class ="list-group-item no-transition miner-error-item">' + data["miners"][i]["errors"][err]["error_message"] + '</div>'
                        };
                        miner_errs_local_html += '</div>'
                    } else {
                        miner_errs_local_html = '<a data-bs-toggle="collapse" href="#errors_' + miner_id_local + '" role="button" class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + data["miners"][i]["ip"] + '<span class="badge bg-fancy-gradient rounded-pill alight-items-middle p-2 m-0" style="width:50px;">' + data["miners"][i]["errors"].length + '</span></a>'
                        miner_errs_local_html += '<div class="collapse no-transition multi-collapse my-0 py-0 ms-5" id="errors_' + miner_id_local + '">'
                        for (err in data["miners"][i]["errors"]) {
                            miner_errs_local_html += '<div class ="list-group-item no-transition miner-error-item">' + data["miners"][i]["errors"][err]["error_message"] + '</div>'
                        };
                        miner_errs_local_html += '</div>'
                    }
                } else {
                    miner_errs_local_html = '<a data-bs-toggle="collapse" href="#errors_' + miner_id_local + '" role="button" class="list-group-item no-transition d-flex justify-content-between list-group-item-action miner-error">' + data["miners"][i]["ip"] + '<span class="badge bg-fancy-gradient rounded-pill alight-items-middle p-2 m-0" style="width:50px;">' + data["miners"][i]["errors"].length + '</span></a>'
                    miner_errs_local_html += '<div class="collapse no-transition multi-collapse my-0 py-0 ms-5" id="errors_' + miner_id_local + '">'
                    for (err in data["miners"][i]["errors"]) {
                        miner_errs_local_html += '<div class ="list-group-item no-transition miner-error-item">' + data["miners"][i]["errors"][err]["error_message"] + '</div>'
                    };
                    miner_errs_local_html += '</div>'
                }
                errors += miner_errs_local_html
            }
        };
    }
}
if (!!errors_card) {
    errors_card.innerHTML = errors
}
