var setDatePickerToday = function() {
    var today = new Date();
    var year = today.getFullYear().toString();
    var month = (today.getMonth() + 1).toString();
    if (month.length == 1) {
        month = "0" + month;
    }
    var day = today.getDate().toString();
    var dateFormat = year + "-" + month + "-" + day;
    document.getElementById("datePicker").value = dateFormat;
}
setDatePickerToday();
