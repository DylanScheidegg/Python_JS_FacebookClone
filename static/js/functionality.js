var count = parseInt(document.getElementById("cookieCount").innerText);
var cursorNumber = parseInt(document.getElementById("cursorCount").innerText);
var grandmaNumber = parseInt(document.getElementById("grandmaCount").innerText);
var farmNumber = parseInt(document.getElementById("farmCount").innerText);
var mineNumber = parseInt(document.getElementById("mineCount").innerText);
var factoryNumber = parseInt(document.getElementById("factoryCount").innerText);
var bankNumber = parseInt(document.getElementById("bankCount").innerText);
var templeNumber = parseInt(document.getElementById("templeCount").innerText);
var wizTowerNumber = parseInt(document.getElementById("wizTowerCount").innerText);
var shipNumber = parseInt(document.getElementById("shipCount").innerText);
var labNumber = parseInt(document.getElementById("labCount").innerText);
var portalNumber = parseInt(document.getElementById("portalCount").innerText);
var timeNumber = parseInt(document.getElementById("timeCount").innerText);
var antiNumber = parseInt(document.getElementById("antiCount").innerText);
var prismNumber = parseInt(document.getElementById("prismCount").innerText);
var chanceNumber = parseInt(document.getElementById("chanceCount").innerText);
var fractalNumber = parseInt(document.getElementById("fractalCount").innerText);
var jsNumber = parseInt(document.getElementById("jsCount").innerText);
var idleverseNumber = parseInt(document.getElementById("idleverseCount").innerText);

var spans = ["cursorCostSpan", "grandmaCostSpan", "farmCostSpan", "mineCostSpan", "factoryCostSpan", "bankCostSpan", "templeCostSpan", "wizTowerCostSpan", "shipCostSpan", "labCostSpan", "portalCostSpan", "timeCostSpan", "antiCostSpan", "prismCostSpan", "chanceCostSpan", "fractalCostSpan", "jsCostSpan","idleverseCostSpan"];
var costs = ["cursorCost", "grandmaCost", "farmCost", "mineCost", "factoryCost", "bankCost", "templeCost", "wizTowerCost", "shipCost", "labCost", "portalCost", "timeCost", "antiCost", "prismCost", "chanceCost", "fractalCost", "jsCost","idleverseCost"];
var boughtNumber = ["cursorNumber", "grandmaNumber", "farmNumber", "mineNumber", "factoryNumber", "bankNumber", "templeNumber", "wizTowerNumber", "shipNumber", "labNumber", "portalNumber", "timeNumber", "antiNumber", "prismNumber", "chanceNumber", "fractalNumber", "jsNumber", "idleverseNumber"];

function clickCookie() {
    count++;
};

function displayCount() {
    document.getElementById("cookieCount").innerText = Math.floor(count);
    document.getElementById("cursorCount").innerText = cursorNumber;
    document.getElementById("grandmaCount").innerText = grandmaNumber;
    document.getElementById("farmCount").innerText = farmNumber;
    document.getElementById("mineCount").innerText = mineNumber;
    document.getElementById("factoryCount").innerText = factoryNumber;
    document.getElementById("bankCount").innerText = bankNumber;
    document.getElementById("templeCount").innerText = templeNumber;
    document.getElementById("wizTowerCount").innerText = wizTowerNumber;
    document.getElementById("shipCount").innerText = shipNumber;
    document.getElementById("labCount").innerText = labNumber;
    document.getElementById("portalCount").innerText = portalNumber;
    document.getElementById("timeCount").innerText = timeNumber;
    document.getElementById("antiCount").innerText = antiNumber;
    document.getElementById("prismCount").innerText = prismNumber;
    document.getElementById("chanceCount").innerText = chanceNumber;
    document.getElementById("fractalCount").innerText = fractalNumber;
    document.getElementById("jsCount").innerText = jsNumber;
    document.getElementById("idleverseCount").innerText = idleverseNumber;

    for (i = 0; i < spans.length; i++) {
        if (count >= document.getElementById(spans[i]).innerText) {
            document.getElementById(costs[i]).disabled = false;
        } else {
            document.getElementById(costs[i]).disabled = true;
        }
    }
};

function countIntervals() {
    count = count + (cursorNumber * 0.1) + (grandmaNumber * 1) + (farmNumber * 8) + (mineNumber * 47) + (factoryNumber * 260) + (bankNumber * 1400) + (templeNumber * 7800) + (wizTowerNumber * 44000) + (shipNumber * 260000) + (labNumber * 1600000) + (portalNumber * 10000000) + (timeNumber * 65000000) + (antiNumber * 430000000) + (prismNumber * 2900000000) + (chanceNumber * 21000000000) + (fractalNumber * 150000000000) + (jsNumber * 1100000000000) + (idleverseNumber * 8300000000000);
};

function buyCursor(cost) {
    for (i = 0; i < spans.length; i++) {
        if (cost == document.getElementById(spans[i]).innerText) {
            if (boughtNumber[i] == "cursorNumber") { cursorNumber += 1; }
            if (boughtNumber[i] == "grandmaNumber") { grandmaNumber += 1; }
            if (boughtNumber[i] == "farmNumber") { farmNumber += 1; }
            if (boughtNumber[i] == "mineNumber") { mineNumber += 1; }
            if (boughtNumber[i] == "factoryNumber") { factoryNumber += 1; }
            if (boughtNumber[i] == "bankNumber") { bankNumber += 1; }
            if (boughtNumber[i] == "templeNumber") { templeNumber += 1; }
            if (boughtNumber[i] == "wizTowerNumber") { wizTowerNumber += 1; }
            if (boughtNumber[i] == "shipNumber") { shipNumber += 1; }
            if (boughtNumber[i] == "labNumber") { labNumber += 1; }
            if (boughtNumber[i] == "portalNumber") { portalNumber += 1; }
            if (boughtNumber[i] == "timeNumber") { timeNumber += 1; }
            if (boughtNumber[i] == "antiNumber") { antiNumber += 1; }
            if (boughtNumber[i] == "prismNumber") { prismNumber += 1; }
            if (boughtNumber[i] == "chanceNumber") { chanceNumber += 1; }
            if (boughtNumber[i] == "fractalNumber") { fractalNumber += 1; }
            if (boughtNumber[i] == "jsNumber") { jsNumber += 1; }
            if (boughtNumber[i] == "idleverseNumber") { idleverseNumber += 1; }

            count -= cost;
            document.getElementById(costs[i]).setAttribute( "onClick", "buyCursor("+Math.floor(document.getElementById(spans[i]).innerText * 1.15)+")" );
            document.getElementById(spans[i]).innerText = Math.floor(document.getElementById(spans[i]).innerText * 1.15);
        }
    }
};

setInterval(countIntervals, 1000);
setInterval(displayCount, 1);