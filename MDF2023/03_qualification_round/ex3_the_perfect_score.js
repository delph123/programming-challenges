// const fs = require("fs");
// const stdinBuffer = fs.readFileSync(0); // STDIN_FILENO = 0
// const input = stdinBuffer.toString().split("\n");
// input.pop();

input = new Array(1000)
    .fill(0)
    .map(() => Math.trunc(Math.random() * 1000))
    .filter((n) => n > 99 && n < 1000)
    .map((n) => n.toString().split(""))
    .map(([a, b, c]) => a + " " + b + " " + c);

ContestResponse();

function ContestResponse() {
    list = input.map((l) => l.split(" ").map((n) => parseInt(n)));

    const candidates = digitsMap();

    const res = list.map(([a, b, c]) => {
        for (let j of candidates.get(a)) {
            if (j + b === c) {
                return [j, b, c].join(" ");
            }
        }

        for (let j of candidates.get(b)) {
            if (a + j === c) {
                return [a, j, c].join(" ");
            }
        }

        for (let j of candidates.get(c)) {
            if (a + b === j) {
                return [a, b, j].join(" ");
            }
        }

        return "Impossible";
    });

    res.forEach((r, i) => {
        console.error("> For", list[i].join(" "));
        console.log(r);
    });
}

function countOneBits(num) {
    return num
        .toString(2)
        .split("")
        .reduce((s, c) => (c === "1" ? s + 1 : s), 0);
}

function digitsMap() {
    // Binary representation of each digit, starting from top right and clockwise
    const digits = [
        0b1111110, 0b1100000, 0b1011011, 0b1110011, 0b1100101, 0b0110111,
        0b0111111, 0b1100010, 0b1111111, 0b1110111,
    ];
    // Create mapping of possible candidates
    const dMap = new Map();
    digits.forEach((dbin, d) => {
        dMap.set(
            d,
            digits
                .map((obin, i) => (countOneBits(dbin ^ obin) === 1 ? i : -1))
                .filter((n) => n >= 0)
        );
    });
    return dMap;
}
