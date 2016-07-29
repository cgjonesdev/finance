var total = 0;
var calcTotal = function() {
    assets = document.getElementsByClassName("assets");
    for (var i=0; i<assets.length; i++) {
       total += parseFloat(assets[i].innerHTML.slice(1, assets[i].innerHTML.length));
       document.getElementById("assetsTotal").innerHTML = "$" + total;
       document.getElementsByClassName("equityAssets")[0].innerHTML = "$" + total;
    }
    total = 0;
    liabilities = document.getElementsByClassName("liabilities");
    for (var i=0; i<liabilities.length; i++) {
       total += parseFloat(liabilities[i].innerHTML.slice(1, liabilities[i].innerHTML.length));
       document.getElementById("liabilitiesTotal").innerHTML = "$" + -total;
       document.getElementsByClassName("equityLiabilities")[0].innerHTML = "$" + -total;
    }
    total = 0;
    equity = document.getElementsByClassName("equity");
    for (var i=0; i<equity.length; i++) {
       total += parseFloat(equity[i].innerHTML.slice(1, equity[i].innerHTML.length));
       document.getElementById("equityTotal").innerHTML = "$" + total;
    }
};
calcTotal();
var monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];
var date = new Date();
dateVal = monthNames[date.getMonth()] + " " + date.getFullYear() + " Balance Sheet"
document.getElementById("monthHeading").innerHTML = dateVal;
document.title = dateVal;

var showAddForm = function(name) {
    addSymbols = document.getElementsByClassName("addSymbol");
    inputs = document.getElementsByTagName("input");
    if (name == "asset") {
        addSymbols[0].src = "/static/assets/minus.png";
    }
    else if (name == "liability") {
        addSymbols[1].src = "/static/assets/minus.png";
    }
    else if (name == "equity") {
        addSymbols[2].src = "/static/assets/minus.png";
    }
    if (name == "asset") {
        document.getElementById("addAssetForm").hidden = !document.getElementById("addAssetForm").hidden
        if (document.getElementById("addAssetForm").hidden) {
            addSymbols[0].src = "/static/assets/add.png";
        }
    }
    else if (name == "liability") {
        document.getElementById("addLiabilityForm").hidden = !document.getElementById("addLiabilityForm").hidden
        if (document.getElementById("addLiabilityForm").hidden) {
            addSymbols[1].src = "/static/assets/add.png";
        }
    }
    else if (name == "equity") {
        document.getElementById("addEquityForm").hidden = !document.getElementById("addEquityForm").hidden
        if (document.getElementById("addEquityForm").hidden) {
            addSymbols[2].src = "/static/assets/add.png";
        }
    }
}

document.addEventListener('mousemove', function(e) {
    activeElement = document.elementFromPoint(e.pageX, e.pageY);
});
images = document.getElementsByTagName("img");
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
