const { part_one, sum, readLines } = require("../../common/aoc");

const fuels = readLines("example");

part_one(unbase5(sum(fuels.map(base5))));

function decimal(d) {
    if (d === "=") return -2;
    if (d === "-") return -1;
    return parseInt(d);
}

function five(d) {
    if (d < 3) return [0, d.toString()];
    if (d === 3) return [1, "="];
    if (d === 4) return [1, "-"];
}

function base5(number) {
    if (number.length === 0) return 0;
    return (
        5 * base5(number.slice(0, number.length - 1)) +
        decimal(number[number.length - 1])
    );
}

function unbase5(n) {
    if (n === 0) return "";
    let [r, l] = five(n % 5);
    return unbase5(Math.floor(n / 5) + r) + l;
}
