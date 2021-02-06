window.onload = () => {
    document.querySelectorAll(".is-success").forEach(item => {
        item.addEventListener("click", confirmBeehive);
    });
}

function confirmBeehive() {
    console.log("Confirm Beehive"); 
    var id = event.srcElement.id.split("_")[1];
    console.log("ID: ", id);
    var statusId = "status_" + id
    var status = document.getElementById(statusId);
    console.log(status.selectedIndex);
    
}
