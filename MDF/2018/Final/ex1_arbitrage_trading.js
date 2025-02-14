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
    const [, trades] = input[0].split(" ").map((n) => parseInt(n));
    const rates = input
        .slice(1)
        .map((l) => l.split(" ").map((a) => parseFloat(a)));

    const start = new Array(rates.length)
        .fill(0)
        .map((_, i) => (i === 0 ? 10000 : 0));

    console.error(trades, rates);

    console.log(maxAmount(rates, trades, start)[0]);
}

function maxAmount(rates, trades, start) {
    let amounts = start;

    for (let t = 0; t < trades; t++) {
        amounts = amounts.map((_, i) => {
            return amounts.reduce((bestTrade, a, j) => {
                return Math.max(bestTrade, a * rates[j][i]);
            }, 0);
        });
    }

    return amounts;
}
