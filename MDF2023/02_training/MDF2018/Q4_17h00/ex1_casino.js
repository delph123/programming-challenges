/*******
 * Read input from STDIN
 * Use: console.log()  to output your result.
 * Use: console.error() to output debug information into STDERR
 * ***/

var input = [];

readline_object.on("line", (value) => {
  //Read input values
  input.push(value);
});
//Call ContestResponse when all inputs are read
readline_object.on("close", ContestResponse);

function ContestResponse() {
  //implement your code here using input array
  // console.log(input)
  const N = parseInt(input[0]);
  const J = parseInt(input[1]);
  const TURNS = input
    .slice(2)
    .map((s) => s.split(" "))
    .map(([a, b, c]) => [parseInt(a), b, parseInt(c)]);

  console.error(N, J);
  //   console.error(TURNS);

  let refill = 0;
  let money = J;

  TURNS.forEach(([a, b, c]) => {
    while (money - a < 0) {
      money += J;
      refill++;
    }

    money += evalResult([a, b, c]) - a;

    console.error([a, b, c], money, refill);
  });

  if (money === 0) {
    refill++;
  }

  console.error("Found:", refill);
  console.log(refill);
}

function evalResult([a, b, c]) {
  if (b === "P") {
    if (c > 0 && c % 2 === 0) {
      return 2 * a;
    } else {
      return 0;
    }
  } else if (b === "I") {
    if (c % 2 === 1) {
      return 2 * a;
    } else {
      return 0;
    }
  } else {
    if (parseInt(b) === c) {
      return 36 * a;
    } else {
      return 0;
    }
  }
}
