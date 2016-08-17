var monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];
var date = new Date();
var dateVal = monthNames[date.getMonth()] + " " + date.getFullYear() + " Budget"
document.getElementById("monthHeading").innerHTML = dateVal;
document.title = dateVal;
