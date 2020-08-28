//Ui state
class State {
  constractor(choicesNames, weightNumber, critiriaNames, matrix, results, numberOfCritiria, choicesNumber, max, weight) {
    this.choicesNames = choicesNames;
    this.weightNumber = weightNumber;
    this.critiriaNames = critiriaNames;
    this.matrix = matrix;
    this.result = results;
    this.numberOfCritiria = numberOfCritiria;
    this.choicesNumber = choicesNumber;
    this.max = max;
    this.weight = weight
  }
}

//handles Ui tasks
class Ui {

  //initialize view
  static initView() {
    let modes = ["start", "numberOfChoices", "choices", "weightNumber", "critiria", "matrix", "result"];
    for (let i = 0; i < modes.length; i++) {
      if (i === 0) {
        document.getElementById(modes[i]).style.display = "visible"
      } else {
        document.getElementById(modes[i]).style.display = "none"
      }
    }
  }
  
  static changeViewModeTo(number) {
    let modes = ["start", "numberOfChoices", "choices", "weightNumber", "critiria", "matrix", "result"];
    for (let i = 0; i < modes.length; i++) {
      if (number === i) {
        document.getElementById(modes[i]).style.display = "unset"
      } else {
        document.getElementById(modes[i]).style.display = "none"
      }
    }
  }
  
  //add row 
  static addChoice() {
    const list = document.getElementById('listChoice');
    let div = document.createElement("div");
    div.innerHTML = ` <div style="margin-top: 10px;"><label>name:</label>
              <li> 
                <input type="text">
              </li></div>`;

    list.appendChild(div);
  }

  //init view choices
  static initViewChoices(number) {
    for (let i =  0; i < number-1; i ++) {
      this.addChoice();
    }
  }

  //make the table
  static initializeCritiriaView(number, numberOfCritiria) {
    let table = document.getElementById('tableDiv');
    let div = document.createElement("div");
    let htmlCode = `<table class="tableClass" id="tableCr">
             <tr>
               <th>Choices</th>
               <th>Name</th>
               <th>Negative</th>`
    for (let i = 0; i < number; i++) {
      if (i === 0) {
        htmlCode = htmlCode + `<th>Weight</th>`
      } else {
        htmlCode = htmlCode + `<th>Weight${i}</th>`
      }
    }
    htmlCode = htmlCode + ` </tr>`
    let trCode = `<tr>
               <td style="text-align:center">-</td>
               <td> <input type="text" class="tableText">  </td>
               <td> <input type="checkbox" ></td>`
    for (let i = 0; i < number; i++) {
      trCode = trCode + `   <td> <input type="number" class="tableText"> </td>`
    }
    trCode = trCode + ` </tr>`;
    for (let i = 0; i < numberOfCritiria; i++) {
      htmlCode = htmlCode + trCode;
    }

    htmlCode = htmlCode + `</table>`;
    div.innerHTML = htmlCode;
    table.appendChild(div);
  }
  
  //make the table
  static initializeMatrix(choiceNames, critiriaNames) {
    let table = document.getElementById('matrixDiv');
    let div = document.createElement("div");
    let htmlCode = `<table class="tableClass" id="matrixTable">
             <tr>
                  <th>Values</th>`;
    let inputCode = ``;
    //make the header of the table and inputs
    for(let i = 0; i < critiriaNames.length; i ++) {
            htmlCode = htmlCode + `<th>${critiriaNames[i]}</th>`;
        inputCode = inputCode + `<td> <input type="number" class="tableText">  </td>`;
    }
    htmlCode = htmlCode + `</tr>`
    //make the rest table
    for(let i=0; i < choiceNames.length; i++) {
        htmlCode = htmlCode + `<tr>` + `<th>${choiceNames[i]}</th>` + inputCode + `</tr>`;
    }
    htmlCode = htmlCode + `</table>`
    div.innerHTML = htmlCode;
    table.appendChild(div);
  }
  
  //make the table
  static initializeResults(results, names, indexes) {
    let table = document.getElementById('resultDiv');
    let div = document.createElement("div");
    let htmlCode = `<table class="tableClass" id="resultTable">
    <tr> 
      <th>Rank</th>
      <th>Name</th>
      <th>Performance</th>
    </tr>`
    console.log(indexes.length)
    console.log(indexes[0])
    for (let i = 0; i < indexes.length; i++ ) {
      htmlCode = htmlCode + `
      <tr>
      <td>${i+1}</td>
      <td>${names[indexes[i]]}</td>
      <td>${results[indexes[i]]}</td>
      </tr>`
    }
    htmlCode = htmlCode + `</table>`
    div.innerHTML = htmlCode;
    table.appendChild(div);
  }
}

//This function is called when buttons nwxt are clicked
function goToNextAndSaveData(number) {
    if (number === 2) {
      let numberOfCh = +document.getElementById("numberOfChoicesText").value;
      state.choicesNumber = numberOfCh;
      Ui.initViewChoices(numberOfCh);
      Ui.changeViewModeTo(2)
    } else if (number === 3) {
      let form = document.getElementById("formChoice").elements;
      var data = [];
      for (let i = 0; i < form.length; i++) {
        data[i] = form[i].value;
      }
      state.choicesNames = data;
      Ui.changeViewModeTo(3);
    } else if (number === 4) {
      let numberOfDms = document.getElementById("numberOfDmsText").value;
      let numberOfCr = document.getElementById("numberOfCriteriaText").value;
      state.weightNumber = numberOfDms;
      state.numberOfCritiria = numberOfCr;
      Ui.initializeCritiriaView(numberOfDms, numberOfCr);
      Ui.changeViewModeTo(4);
    } else if (number === 5) {
      let crTable = document.getElementById("critiriaForm").elements;
      saveCritiria(crTable)
      Ui.initializeMatrix(state.choicesNames, state.critiriaNames)
      Ui.changeViewModeTo(5);
    } else if (number === 6) {
      let matrix = document.getElementById("matrixForm").elements;  
      console.log(matrix);
      saveMatrix(matrix);
      getResults();
    }
}

//save the matrix data
function saveMatrix(matrix) {
    let numberOfColum = state.critiriaNames.length;
    let values = [];
    let matrixValues = [];
    let number = 1;
    for (let i = 0; i < matrix.length; i++) {
      values.push(+matrix[i].value);
      if (i+1 === numberOfColum * number) {
          matrixValues.push(values);
        values = [];
        number ++;
      }
    }
    state.matrix = matrixValues;
}
    
function saveCritiria(elements) {
    let numberOfCr =  +state.numberOfCritiria;
    let numberOfValuesRow = +state.weightNumber + 2 ;
    console.log(numberOfValuesRow);
    let namesArray = [];
    let weightArray = [];
    let maxArray = [];
    let nameIndex = 0;
    let array = [];
    for (let i = 0; i < elements.length; i++) {
        if (i === nameIndex) {
          if (i !== 0) weightArray.push(array);
        array = [];
          namesArray.push(elements[i].value);
      } else if (i === nameIndex + 1) {
          nameIndex = nameIndex + numberOfValuesRow;
        if (elements[i].checked === false) {
            maxArray.push(true)
        } else {
            maxArray.push(false)
        }
      } else {
        array.push(+elements[i].value);
      }
    }
    
    weightArray.push(array);
    let finalArray = [];
    //make the correct weight array
    for (let i = 0; i < +state.weightNumber; i++) {
      array = [];
        for (let a = 0 ; a < weightArray.length; a++) {
          array.push(weightArray[a][i]);
      }
      finalArray.push(array);
    }
    state.critiriaNames = namesArray;
    state.max = maxArray;
    state.weight = finalArray;
    
}

//get values for the backend
function getResults() {
  let multiWeight = false;
  if (state.weightNumber > 1) multiWeight = true;
  eel.topsis_capulate(state.matrix, state.weight, state.max, multiWeight)(function(ret) {
    console.log(state.choicesNames)
    Ui.initializeResults(ret[0], state.choicesNames, ret[1])
    Ui.changeViewModeTo(6);});
}

//start from the beggining
function reset() {
  state = new State(null, null, null, null, null, null, null, null, null);
  Ui.changeViewModeTo(0);
}

//init
var state = new State(null, null, null, null, null, null, null, null, null);
Ui.initView();