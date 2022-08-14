$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#rec_id").val(res.id);
        $("#rec_product_id").val(res.product_id);
        $("#rec_product_name").val(res.product_name);
        $("#rec_rec_id").val(res.rec_id);
        $("#rec_rec_name").val(res.rec_name);
        $("#rec_rec_type").val(res.rec_type);
        $("#rec_like_num").val(res.like_num);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#rec_product_id").val('');
        $("#rec_product_name").val('');
        $("#rec_rec_id").val('');
        $("#rec_rec_name").val('');
        $("#rec_rec_type").val('');
        $("#rec_like_num").val('');
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Recommendation
    // ****************************************

    $("#create-btn").click(function () {

        let id = parseInt($("#rec_id").val());
        let productId = parseInt($("#rec_product_id").val());
        let productName = $("#rec_product_name").val();
        let recId = parseInt($("#rec_rec_id").val());
        let recName = $("#rec_rec_name").val();
        let recType = $("#rec_rec_type").val();
        let likeNum = parseInt($("#rec_like_num").val());

        let data = {
            "id": id,
            "product_id": productId,
            "product_name": productName,
            "rec_id": recId,
            "rec_name": recName,
            "rec_type": recType,
            "like_num": likeNum
        };

        $("#flash_message").empty();
        console.log(data)
        let ajax = $.ajax({
            type: "POST",
            url: "/api/recommendations",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Recommendation
    // ****************************************

    $("#update-btn").click(function () {

        let id = parseInt($("#rec_id").val());
        let productId = parseInt($("#rec_product_id").val());
        let productName = $("#rec_product_name").val();
        let recId = parseInt($("#rec_rec_id").val());
        let recName = $("#rec_rec_name").val();
        let recType = $("#rec_rec_type").val();
        let likeNum = parseInt($("#rec_like_num").val());

        let data = {
            "id": id,
            "product_id": productId,
            "product_name": productName,
            "rec_id": recId,
            "rec_name": recName,
            "rec_type": recType,
            "like_num": likeNum
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/recommendations/${id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Like a Recommendation
    // ****************************************

    $("#like-btn").click(function () {

        let id = parseInt($("#rec_id").val());
        let productId = parseInt($("#rec_product_id").val());
        let productName = $("#rec_product_name").val();
        let recId = parseInt($("#rec_rec_id").val());
        let recName = $("#rec_rec_name").val();
        let recType = $("#rec_rec_type").val();
        let likeNum = parseInt($("#rec_like_num").val());

        let data = {
            "id": id,
            "product_id": productId,
            "product_name": productName,
            "rec_id": recId,
            "rec_name": recName,
            "rec_type": recType,
            "like_num": likeNum
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/recommendations/${id}/like`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });    

    // ****************************************
    // Unlike a Recommendation
    // ****************************************

    $("#unlike-btn").click(function () {

        let id = parseInt($("#rec_id").val());
        let productId = parseInt($("#rec_product_id").val());
        let productName = $("#rec_product_name").val();
        let recId = parseInt($("#rec_rec_id").val());
        let recName = $("#rec_rec_name").val();
        let recType = $("#rec_rec_type").val();
        let likeNum = parseInt($("#rec_like_num").val());

        let data = {
            "id": id,
            "product_id": productId,
            "product_name": productName,
            "rec_id": recId,
            "rec_name": recName,
            "rec_type": recType,
            "like_num": likeNum
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/recommendations/${id}/unlike`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    }); 

    // ****************************************
    // Retrieve a Recommendation
    // ****************************************

    $("#retrieve-btn").click(function () {

        let rec_id = $("#rec_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/recommendations/${rec_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Recommendation
    // ****************************************

    $("#delete-btn").click(function () {

        let rec_id = $("#rec_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/recommendations/${rec_id}`,
            // contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Recommendation has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#rec_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Recommendation
    // ****************************************

    $("#search-btn").click(function () {

        let product_id = $("#rec_product_id").val();
        let rec_type = $("#rec_rec_type").val();
        let queryString = ""

        if (product_id) {
            if (queryString.length > 0) {
                queryString += '&product_id=' + product_id
            } else {
                queryString += 'product_id=' + product_id
            }
        }
        if (rec_type) {
            if (queryString.length > 0) {
                queryString += '&rec_type=' + rec_type
            } else {
                queryString += 'rec_type=' + rec_type
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/recommendations?${queryString}`,
            // contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Product ID</th>'
            table += '<th class="col-md-2">Product Name</th>'
            table += '<th class="col-md-2">Rec ID</th>'
            table += '<th class="col-md-2">Rec Name</th>'
            table += '<th class="col-md-2">Rec Type</th>'
            table += '<th class="col-md-2">Like</th>'
            table += '</tr></thead><tbody>'
            let firstRec = "";
            for(let i = 0; i < res.length; i++) {
                let rec = res[i];
                table +=  `<tr id="row_${i}"><td>${rec.id}</td><td>${rec.product_id}</td>
                <td>${rec.product_name}</td><td>${rec.rec_id}</td><td>${rec.rec_name}</td>
                <td>${rec.rec_type}</td><td>${rec.like_num}</td></tr>`;
                if (i == 0) {
                    firstRec = rec;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstRec != "") {
                update_form_data(firstRec)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
