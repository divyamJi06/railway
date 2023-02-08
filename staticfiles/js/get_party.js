// allID = "party";
document.getElementById("party_name").addEventListener("input",handleInput)
console.log("GGGGGGGEEEEEEEEEETTTTTTTTPPPPPAAAARRRRRTTYYYYYYYY");
async function handleInput() {
  const inputValue = this.value;
  allID = this.id.split("_")[0];
  console.log(allID);
  console.log(allID);
  if (inputValue.length < 3) {
    document.getElementById("message").innerHTML = `Enter atleast 3 letters`;
    return;
  }
  document.getElementById(`${allID}_suggestions`).style.display = "none";
  const partySuggestions = await getPartySuggestions(inputValue,allID);
  if (partySuggestions.length == 0) {
    alink = `<a href="/bilti/add_party">here</a>`;
    document.getElementById(
      "message"
    ).innerHTML = `No party found. Add it ${alink}`;
    return;
  }
  document.getElementById("message").innerHTML = "";
  console.log(partySuggestions);
  const suggestionsContainer = document.getElementById(`${allID}_suggestions`);
  let suggestionsHTML = "";
  // partysListUpdated = partySuggestions;
  partySuggestions.forEach((suggestion) => {
    suggestionsContainer.appendChild(addSuggestions(suggestion,allID));
  });
  console.log(suggestionsHTML);
  suggestionsContainer.style.display = "block";
}

function selectParty(selectedSuggestion,allID) {
  // if(selectedSuggestion)
  console.log(selectedSuggestion);
  console.log("scsc");
  console.log(`${allID}_suggestions`)
  document.getElementById(`${allID}_suggestions`).style.display = "none";
  //   return;

  document.getElementById(`${allID}_name`).value = selectedSuggestion.innerHTML;
  document.getElementById(`${allID}_name`).setAttribute("readonly", true);
  document.getElementById(`${allID}_address`).value =
    selectedSuggestion.dataset.address;
  document.getElementById(`${allID}_id`).value =
    selectedSuggestion.dataset.address;
  document.getElementById(`${allID}_gst`).value =
    selectedSuggestion.dataset.gst;

  document.getElementById(`${allID}_details`).style.display = "block";

  console.log(selectedSuggestion);
  document.getElementById(`${allID}_id`).value = selectedSuggestion.dataset.id;
}
function editParty(allID) {
  document.getElementById(`${allID}_name`).removeAttribute("readonly");
  document.getElementById(`${allID}_details`).style.display = "none";
}

async function getPartySuggestions(inputValue) {
  if (inputValue.length >= 3) {
    console.log("DBvaba")
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
    console.log(response);
    return response["partys"];
  }
  return [];
}

function addSuggestions(suggestion,allID) {
  const suggestionDiv = document.createElement("div");
  suggestionDiv.setAttribute("class", "suggestion");
  suggestionDiv.setAttribute("data-id", suggestion.id);
  suggestionDiv.setAttribute("data-address", suggestion.address);
  suggestionDiv.setAttribute("data-gst", suggestion.gst);
  suggestionDiv.setAttribute("data-name", suggestion.name);
  suggestionDiv.innerHTML = suggestion.name;
  suggestionDiv.onclick = function () {
    selectParty(this,allID);
  };
  suggestionDiv.style.cursor = "pointer";
  console.log(suggestionDiv);
  return suggestionDiv;
}
