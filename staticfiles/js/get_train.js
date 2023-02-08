document
  .getElementById("train_number")
  .addEventListener("input", handleTrainNo);


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

  function editTrain(allID) {
    document.getElementById(`${allID}_number`).removeAttribute("readonly");
    document.getElementById(`${allID}_details`).style.display = "none";
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