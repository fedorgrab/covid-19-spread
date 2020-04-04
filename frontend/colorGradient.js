color1 = [8, 211, 38];
color2= [224, 2, 9];

function interpolateColor(factor) {
  // if (arguments.length < 3) {
  //   factor = 0.5;
  // }
  var result = color1.slice();
  for (var i = 0; i < 3; i++) {
    result[i] = Math.round(result[i] + factor * (color2[i] - color1[i]));
  }
  return `rgb(${result[0]}, ${result[1]}, ${result[2]})`
}


// GRADIENT_FROM = [24, 224, 54];
// GRADIENT_TO = [224, 2, 9];
//
// function interpolateColor(factor) {
//   let result = GRADIENT_FROM;
//   for (var i = 0; i < 3; i++) {
//     result[i] = Math.round(result[i] + factor * (GRADIENT_TO[i] - GRADIENT_FROM[i]));
//   }
//   return `rgb(${result[0]}, ${result[1]}, ${result[2]})`
// }
