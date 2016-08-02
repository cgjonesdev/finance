var total = 0;
var calcTotal = function() {
    var assets = document.getElementsByClassName("assets");
    for (var i=0; i<assets.length; i++) {
       total += parseFloat(assets[i].innerHTML.slice(1, assets[i].innerHTML.length));
       document.getElementById("assetsTotal").innerHTML = "$" + total;
       // document.getElementsByClassName("equityAssets")[0].innerHTML = "$" + total;
    }
    total = 0;
    var liabilities = document.getElementsByClassName("liabilities");
    for (var i=0; i<liabilities.length; i++) {
       total += parseFloat(liabilities[i].innerHTML.slice(1, liabilities[i].innerHTML.length));
       document.getElementById("liabilitiesTotal").innerHTML = "$" + -total;
       // document.getElementsByClassName("equityLiabilities")[0].innerHTML = "$" + -total;
    }
    total = 0;
    var equity = document.getElementsByClassName("equity");
    for (var i=0; i<equity.length; i++) {
       total += parseFloat(equity[i].innerHTML.slice(1, equity[i].innerHTML.length));
       // document.getElementById("equityTotal").innerHTML = "$" + total;
    }
};
calcTotal();
var monthNames = ["January", "February", "March", "April", "May", "June",
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
    submitAsset.value = "Add";
    submitAsset.style.background = "linear-gradient(rgb(95,205,85), rgb(40,120,25))";
    submitLiability.value = "Add";
    submitLiability.style.background = "linear-gradient(rgb(95,205,85), rgb(40,120,25))";
    submitEquity.value = "Add";
    submitEquity.style.background = "linear-gradient(rgb(95,205,85), rgb(40,120,25))";
    if (name == "asset") {
        addSymbols[0].src = "/static/assets/minus.png";
    }
    else if (name == "liability") {
        addSymbols[1].src = "/static/assets/minus.png";
    }
    else if (name == "equity") {
        addSymbols[2].src = "/static/assets/minus.png";
    }
    var form = document.getElementById("addEditAssetForm");
    form.reset();
    if (name == "asset") {
        form.hidden = !form.hidden
        if (form.hidden) {
            addSymbols[0].src = "/static/assets/add.png";
        }
    }
    var form = document.getElementById("addEditLiabilityForm");
    form.reset();
    if (name == "liability") {
        form.hidden = !form.hidden
        if (form.hidden) {
            addSymbols[1].src = "/static/assets/add.png";
        }
    }
    var form = document.getElementById("addEditEquityForm");
    form.reset();
    if (name == "equity") {
        form.hidden = !form.hidden
        if (form.hidden) {
            addSymbols[2].src = "/static/assets/add.png";
        }
    }
}

document.addEventListener('mousemove', function(e) {
    activeElement = document.elementFromPoint(e.pageX, e.pageY);
});

var showEditForm = function(name, amount) {
    addSymbols = document.getElementsByClassName("addSymbol");
    if (name == "asset") {
        var form = document.getElementById("addEditAssetForm");
        form.hidden = !form.hidden
        var submitAsset = document.getElementById("submitAsset");
        submitAsset.value = "Edit";
        var assetName = document.getElementById("addAssetName");
        assetName.value = activeElement.name;
        var assetAmount = document.getElementById("addAssetAmount");
        assetAmount.value = parseFloat(amount);
        submitAsset.style.background = "linear-gradient(rgb(245,229,10), rgb(165,160,60))";
        addSymbols[0].src = "/static/assets/add.png";
        form.action = "/balance_sheet/" + activeElement.name + "/update";
    }
    if (name == "liability") {
        var form = document.getElementById("addEditLiabilityForm");
        form.hidden = !form.hidden
        var submitLiability = document.getElementById("submitLiability");
        submitLiability.value = "Edit";
        var liabilityName = document.getElementById("addLiabilityName");
        liabilityName.value = activeElement.name;
        var liabilityAmount = document.getElementById("addLiabilityAmount");
        liabilityAmount.value = parseFloat(amount);
        submitLiability.style.background = "linear-gradient(rgb(245,229,10), rgb(165,160,60))";
        addSymbols[1].src = "/static/assets/add.png";
        form.action = "/balance_sheet/" + activeElement.name + "/update";
    }
    if (name == "equity") {
        var form = document.getElementById("addEditEquityForm");
        form.hidden = !form.hidden
        var submitEquity = document.getElementById("submitEquity");
        submitEquity.value = "Edit";
        var equityName = document.getElementById("addEquityName");
        equityName.value = activeElement.name;
        var equityAmount = document.getElementById("addEquityAmount");
        equityAmount.value = parseFloat(amount);
        submitEquity.style.background = "linear-gradient(rgb(245,229,10), rgb(165,160,60))";
        addSymbols[2].src = "/static/assets/add.png";
        form.action = "/balance_sheet/" + activeElement.name + "/update";
    }
}

var showDelete = function(name) {
    var answer = confirm("Are you sure you want to delete " + activeElement.name + "?");
    if (answer) {
        window.location = "/balance_sheet/" + activeElement.name + "/delete";
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
