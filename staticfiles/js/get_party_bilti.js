document
  .getElementById("consignee_name")
  .addEventListener("input", handleInput);
document
  .getElementById("consignor_name")
  .addEventListener("input", handleInput);
document
  .getElementById("train_number")
  .addEventListener("input", handleTrainNo);

var now = new Date();
now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
document.getElementById("bill_date").value = now.toISOString().slice(0, 16);
// document.querySelector("input[name=bill_date]").value = today;

function calculateTotal() {
  var weightPerPackage = parseFloat(
    document.getElementById("weight-per-package").value
  );
  console.log(weightPerPackage);
  var pricePerWeight = parseFloat(
    document.getElementById("price-per-weight").value
  );
  // if(pricePerWeight && weightPerPackage){
  document.getElementById("bill_amount_details").style.display = "block";

  if (
    !(Number.isInteger(weightPerPackage) && Number.isInteger(pricePerWeight))
  ) {
    document.getElementById("total-amount").value = 0;
    document.getElementById("total-bill").value = 0;
    return;
  }
  var totalAmount = weightPerPackage * pricePerWeight;
  var totalBill = totalAmount * 1.05;

  document.getElementById("total-amount").value = totalAmount.toFixed(2);
  document.getElementById("total-bill").value = totalBill.toFixed(2);
}
async function handleTrainNo() {
  const inputValue = this.value;
  allID = this.id.split("_")[0];

  if (inputValue.length >= 1) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/bilti/check_train?train_number=" + inputValue, true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.send();
    const response = await new Promise((resolve, reject) => {
      xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          resolve(JSON.parse(xhr.responseText));
        }
      };
    });
    console.log(response);
    partySuggestions = response["partys"];
    if (partySuggestions.length == 0) {
      alink = `<a href="/bilti/add_train">here</a>`;
      document.getElementById(
        "message"
      ).innerHTML = `No trains found. Add it ${alink}`;
      const suggestionsContainer = document.getElementById(
        `${allID}_suggestions`
      );
      suggestionsContainer.innerHTML = "";
      return;
    }
    document.getElementById("message").innerHTML = "";
    const suggestionsContainer = document.getElementById(
      `${allID}_suggestions`
    );
    suggestionsContainer.innerHTML = "";
    partySuggestions.forEach((suggestion) => {
      suggestionsContainer.appendChild(addSuggestionsTrains(suggestion, allID));
    });
    suggestionsContainer.style.display = "block";
  }
  return [];
}
async function handleInput() {
  const inputValue = this.value;
  allID = this.id.split("_")[0];

  if (inputValue.length < 3) {
    document.getElementById("message").innerHTML = `Enter atleast 3 letters`;
    return;
  }
  document.getElementById(`${allID}_suggestions`).style.display = "none";
  const partySuggestions = await getPartySuggestions(inputValue, allID);
  if (partySuggestions.length == 0) {
    alink = `<a href="/bilti/add_party">here</a>`;
    document.getElementById(
      "message"
    ).innerHTML = `No party found. Add it ${alink}`;
    return;
  }
  document.getElementById("message").innerHTML = "";
  const suggestionsContainer = document.getElementById(`${allID}_suggestions`);
  suggestionsContainer.innerHTML = "";
  partySuggestions.forEach((suggestion) => {
    idOfConsignorOrConsignee =
      allID === "consignee"
        ? document.getElementById("consignor_id").value
        : document.getElementById("consignee_id").value;
    // console.log(suggestion.id);
    // console.log(idOfConsignorOrConsignee);
    if (suggestion.id != idOfConsignorOrConsignee) {
      suggestionsContainer.appendChild(addSuggestions(suggestion, allID));
    }
  });
  suggestionsContainer.style.display = "block";
}

function selectParty(selectedSuggestion, allID) {
  document.getElementById(`${allID}_suggestions`).style.display = "none";

  document.getElementById(`${allID}_name`).value = selectedSuggestion.innerHTML;
  document.getElementById(`${allID}_name`).setAttribute("readonly", true);
  document.getElementById(`${allID}_address`).value =
    selectedSuggestion.dataset.address;
  document.getElementById(`${allID}_id`).value =
    selectedSuggestion.dataset.address;
  document.getElementById(`${allID}_gst`).value =
    selectedSuggestion.dataset.gst;

  document.getElementById(`${allID}_details`).style.display = "block";
  document.getElementById(`${allID}_id`).value = selectedSuggestion.dataset.id;
}

function selectTrain(selectedSuggestion, allID) {
  document.getElementById(`${allID}_suggestions`).style.display = "none";

  document.getElementById(`${allID}_name`).value =
    selectedSuggestion.dataset.name;
  document.getElementById(`${allID}_name`).setAttribute("readonly", true);

  document.getElementById(`${allID}_details`).style.display = "block";
  document.getElementById(`${allID}_number`).value =
    selectedSuggestion.innerHTML;
  document.getElementById(`${allID}_number`).setAttribute("readonly", true);
}
function editParty(allID) {
  document.getElementById(`${allID}_name`).removeAttribute("readonly");
  document.getElementById(`${allID}_details`).style.display = "none";
}
function editTrain(allID) {
  document.getElementById(`${allID}_number`).removeAttribute("readonly");
  document.getElementById(`${allID}_details`).style.display = "none";
}

async function getPartySuggestions(inputValue) {
  if (inputValue.length >= 3) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/bilti/check_party?party_name=" + inputValue, true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.send();
    const response = await new Promise((resolve, reject) => {
      xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          resolve(JSON.parse(xhr.responseText));
        }
      };
    });
    // console.log(response);
    return response["partys"];
  }
  return [];
}

function addSuggestions(suggestion, allID) {
  const suggestionDiv = document.createElement("div");
  suggestionDiv.setAttribute("class", "suggestion");
  suggestionDiv.setAttribute("data-id", suggestion.id);
  suggestionDiv.setAttribute("data-address", suggestion.address);
  suggestionDiv.setAttribute("data-gst", suggestion.gst);
  suggestionDiv.setAttribute("data-name", suggestion.name);
  suggestionDiv.innerHTML = suggestion.name;
  suggestionDiv.onclick = function () {
    selectParty(this, allID);
  };
  suggestionDiv.style.cursor = "pointer";
  //   console.log(suggestionDiv);
  return suggestionDiv;
}

function addSuggestionsTrains(suggestion, allID) {
  const suggestionDiv = document.createElement("div");
  suggestionDiv.setAttribute("class", "suggestion");
  suggestionDiv.setAttribute("data-name", suggestion.name);
  suggestionDiv.innerHTML = suggestion.number;
  suggestionDiv.onclick = function () {
    selectTrain(this, allID);
  };
  suggestionDiv.style.cursor = "pointer";
  //   console.log(suggestionDiv);
  return suggestionDiv;
}
