var monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];
var date = new Date();
var dateVal = monthNames[date.getMonth()] + " " + date.getFullYear() + " Budget"
document.getElementById("monthHeading").innerHTML = dateVal;
document.title = dateVal;

var showTimeFrameSelectorInfo = function() {
    document.getElementById("assetSwitchAnswer").style.display = "inline";
}

var hideTimeFrameSelectorInfo = function() {
    document.getElementById("assetSwitchAnswer").style.display = "none";
}

var options = document.getElementsByTagName("select")[0].options;
var timeframeSelected = function() {
    var timeFrame = options[options.selectedIndex].value
    if (timeFrame == "default (monthly)") {
        window.location = "/budget/monthly";
    }
    else {
        window.location = "/budget/" + timeFrame;
    }
}

pathnameArray = window.location.pathname.split("/");
time_frame = pathnameArray[pathnameArray.length - 1];
for (var i=0; i < options.length; i++) {
    if (options[i].innerHTML == time_frame) {
        options[i].selected = time_frame;
        document.getElementById("assetSwitchQuestion").style.display = "none";
    }
}
