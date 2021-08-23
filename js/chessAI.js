//Values are arbitrary, taken from Sebastian Lague's video (https://www.youtube.com/watch?v=U4ogK0MIzqk&t=42s)
var pawnValue = 100;
var knightValue = 300;
var bishopValue = 300;
var rookValue = 500;
var queenValue = 900;

//Overral Evaluation Function
function evaluate() {
  var whiteEval = addValues("w");
  var blackEval = addValues("b");

  console.log(whiteEval - blackEval);

  return whiteEval - blackEval;
}

function addValues(color){
  
  //This feels janky but its easier to understand this way. Deletes all non-piece FEN charactersz
  var fenRef = board.fen();
  var reMain = new RegExp(/\/| |K|k|-|w|0|1|2|3|4|5|6|7|8|9/, "g")
  fenRef = String(fenRef).replace(reMain, "");

  //Only keeps the FEN characters of each side
  if (color == "w") {
    var reWhite = new RegExp(/p|n|b|r|q/, "g");
    fenRef = fenRef.replace(reWhite, "");
  }
  else {
    var reBlack = new RegExp(/P|N|B|R|Q/, "g");
    fenRef = fenRef.replace(reBlack, "");
    
  }
  //console.log(fenRef);

  var score = 0;
  fenRef = fenRef.toLowerCase();

  //Adds up total side score
  for (var i = 0; i < fenRef.length; i++){
    switch(fenRef.charAt(i)){
      case "p":
        score += pawnValue;
        break;
      case "n":
        score += knightValue;
        break;
      case "b":
        score += bishopValue;
        break;
      case "r":
        score += rookValue;
        break;
      case "q":
        score += queenValue;
        break;
    }
  }
  //console.log(score);
  
  return score;
}