var monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];
var date = new Date();
var dateVal = monthNames[date.getMonth()] + " " + date.getFullYear() + " Balance Sheet"
document.getElementById("monthHeading").innerHTML = dateVal;
document.title = dateVal;

var showAddForm = function(name) {
    var addSymbols = document.getElementsByClassName("addSymbol");
    var inputs = document.getElementsByTagName("input");
    var submitAsset = document.getElementById("submitAsset");
    if (name == "asset") {
        submitAsset.value = "Add";
        submitAsset.style.background = "linear-gradient(rgb(95,205,85), rgb(40,120,25))";
        addSymbols[0].style.display = "none";
    }
    else if (name == "liability") {
        submitLiability.value = "Add";
        submitLiability.style.background = "linear-gradient(rgb(95,205,85), rgb(40,120,25))";
        addSymbols[1].style.display = "none";
    }
    else if (name == "equity") {
        submitEquity.value = "Add";
        submitEquity.style.background = "linear-gradient(rgb(95,205,85), rgb(40,120,25))";
        addSymbols[2].style.display = "none";
    }
    if (name == "asset") {
        var form = document.getElementById("addEditAssetForm");
        form.reset();
        form.hidden = !form.hidden
        if (form.hidden) {
            addSymbols[0].src = "/static/assets/add.png";
        }
    }
    if (name == "liability") {
        var form = document.getElementById("addEditLiabilityForm");
        form.reset();
        form.hidden = !form.hidden
        if (form.hidden) {
            addSymbols[1].src = "/static/assets/add.png";
        }
    }
    if (name == "equity") {
        var form = document.getElementById("addEditEquityForm");
        form.reset();
        form.hidden = !form.hidden
        if (form.hidden) {
            addSymbols[2].src = "/static/assets/add.png";
        }
    }
    form.style.display = "inline";
    form.style.marginBottom = "1em";
}

var cancelAddEdit = function(name) {
    var addSymbols = document.getElementsByClassName("addSymbol");
    if (name == "asset") {
        var form = document.getElementById("addEditAssetForm");
        addSymbols[0].style.display = "inline";
    }
    else if (name == "liability") {
        var form = document.getElementById("addEditLiabilityForm");
        addSymbols[1].style.display = "inline";
    }
    else if (name == "equity") {
        var form = document.getElementById("addEditEquityForm");
        addSymbols[2].style.display = "inline";
    }
    form.action = "/balance_sheet";
    form.style.display = "none";
    form.style.marginBottom = "1em";
}

document.addEventListener('mousemove', function(e) {
    activeElement = document.elementFromPoint(e.pageX, e.pageY);
    console.log(activeElement.name);
});

var showDetailPage = function(name, _id) {
    window.location = "/balance_sheet/" + _id;
}

var showEditForm = function(name, _id, amount) {
    addSymbols = document.getElementsByClassName("addSymbol");
    if (name == "asset") {
        var form = document.getElementById("addEditAssetForm");
        form.hidden = !form.hidden
        var submitAsset = document.getElementById("submitAsset");
        submitAsset.value = "Edit";
        var assetName = document.getElementById("addAssetName");
        assetName.value = activeElement.name;
        var assetAmount = document.getElementById("addAssetAmount");
        assetAmount.value = amount;
        submitAsset.style.background = "linear-gradient(rgb(245,229,10), rgb(165,160,60))";
        addSymbols[0].style.display = "none";
        form.action = "/balance_sheet/" + _id + "/update";
    }
    if (name == "liability") {
        var form = document.getElementById("addEditLiabilityForm");
        form.hidden = !form.hidden
        var submitLiability = document.getElementById("submitLiability");
        submitLiability.value = "Edit";
        var liabilityName = document.getElementById("addLiabilityName");
        liabilityName.value = activeElement.name;
        var liabilityAmount = document.getElementById("addLiabilityAmount");
        liabilityAmount.value = -amount;
        submitLiability.style.background = "linear-gradient(rgb(245,229,10), rgb(165,160,60))";
        addSymbols[1].style.display = "none";
        form.action = "/balance_sheet/" + _id + "/update";
    }
    if (name == "equity") {
        var form = document.getElementById("addEditEquityForm");
        form.hidden = !form.hidden
        var submitEquity = document.getElementById("submitEquity");
        submitEquity.value = "Edit";
        var equityName = document.getElementById("addEquityName");
        equityName.value = activeElement.name;
        var equityAmount = document.getElementById("addEquityAmount");
        equityAmount.value = amount;
        submitEquity.style.background = "linear-gradient(rgb(245,229,10), rgb(165,160,60))";
        addSymbols[2].style.display = "none";
        form.action = "/balance_sheet/" + _id + "/update";
    }
    form.style.display = "inline";
    form.style.marginBottom = "1em";
}

var showDelete = function(name, _id) {
    var answer = confirm("Are you sure you want to delete " + activeElement.name + "?");
    if (answer) {
        window.location = "/balance_sheet/" + _id + "/delete";
    }
}

var images = document.getElementsByTagName("img");
var showPencil = function(name) {
    for (var i=0; i<images.length; i++) {
        if (images[i].name == name) {
            images[i].style.display = "inline";
        }
    }
}
var hidePencil = function(name) {
    for (var i=0; i<images.length; i++) {
        if (images[i].name == name) {
            images[i].style.display = "none";
        }
    }
}

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
        window.location = "/balance_sheet/monthly";
    }
    else {
        window.location = "/balance_sheet/" + timeFrame;
    }
}

var sessionTimeFrame = document.getElementById("sessionTimeFrame").innerHTML;
var pathnameArray = window.location.pathname.split("/");
var timeFrame = pathnameArray[pathnameArray.length - 1];

for (var i=0; i < options.length; i++) {
    if (options[i].innerHTML == timeFrame) {
        options[i].selected = timeFrame;
        console.log("timeFrame");
        document.getElementById("assetSwitchQuestion").style.display = "none";
    }
}

