const params = "3 3 5";
let [c, r, s] = params.split(" ").map((i) => parseInt(i));

console.log("Drawing diamonds", c, r, s);

let diam = [];

for (let i = 0; i < s; i++) {
  diam.push(
    "".concat(
      ..."."
        .repeat(s - i - 1)
        .concat("/")
        .concat(
          "*"
            .repeat(2 * i)
            .concat("\\")
            .concat(".".repeat(s - i - 1))
        )
    )
  );
}

for (let i = s - 1; i >= 0; i--) {
  diam.push(
    "".concat(
      ..."."
        .repeat(s - i - 1)
        .concat("\\")
        .concat(
          "*"
            .repeat(2 * i)
            .concat("/")
            .concat(".".repeat(s - i - 1))
        )
    )
  );
}

const gem = diam.map((l) => "".concat(...new Array(c).fill(l)));

for (let i = 1; i < r; i++) {
  for (let j = 0; j < diam.length; j++) {
    gem.push(gem[j]);
  }
}

const final = "".concat(...gem.map((l) => l + "\n"));
console.log(final);

const md5 = require("md5");
console.log(md5(final));
