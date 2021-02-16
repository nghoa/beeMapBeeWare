window.onload = () => {
    document.querySelectorAll(".is-success").forEach(item => {
        item.addEventListener("click", confirmBeehive);
    });

    document.querySelectorAll(".is-info").forEach(item => {
        item.addEventListener("click", toggleTable);
    });

    $(".modal-close").click(function() {
        $(".modal").removeClass("is-active");
    });

}



function toggleTable(e) {
    var test = e.target.id.split("_");
    var eventId = e.target.id.split("_")[1];
    var longitude = e.target.id.split("_")[2];
    var latitude = e.target.id.split("_")[3];
    var targetName = "#target_" + eventId;
    var mapName = "#map_" + eventId;
    // $("#mapContent").load("map")
    
    var route = "map?" + "lon=" + longitude + "&lat=" + latitude + "&id=" + eventId

    $(targetName).toggle('slow');
    $(mapName).load(route);
}


function confirmBeehive(e) {
    var eventId = e.target.id.split("_")[1];
    // console.log("ID: ", eventId);
    var statusId = "status_" + eventId;
    var selectedStatus = $("#"+ statusId + " option:selected").val();
    // console.log('selectedText: ', selectedStatus);

    // roundabout way to sent boolean values to server side
    // 1 and 0 are more consistent than string with True and False
    if (selectedStatus == '1' || selectedStatus == 1) {
        var sentStatus = "1"
    } else {
        var sentStatus = "0"
    }

    resp = {"id": eventId, "status": sentStatus};

    $.ajax({
        type : "POST",
        url : '/admin/dashboard/update-status',
        dataType: "text",
        data: JSON.stringify(resp),
        contentType: 'application/json;charset=UTF-8',
        success: ajax_success,
        error: ajax_error
        });
}

function ajax_success() {
    console.log('Update Status worked');
    // Trigger Modal after success
    // TODO: 
    // improve loading time of ajax request because modal is loading to slow
    $(".modal").addClass("is-active");  
}


/**
 * Catch the ajax error
 */
function ajax_error(xhr, status, error) {
    console.log("Error: " + error);
    console.log("Status: " + status);
    console.log(xhr);
}
