const fs = require("fs");
const stdinBuffer = fs.readFileSync(0); // STDIN_FILENO = 0
const input = stdinBuffer.toString().split("\n");
input.pop();

ContestResponse();

function ContestResponse() {
    console.error(input);

    let subs = input.slice(1).map((s) => s.split(" "));
    subs = subs.map(([a, b]) => [parseInt(a), b]);

    const hashes = subs
        .map(([a, b]) => b)
        .reduce((prev, curr) => {
            if (prev.has(curr)) {
                prev.set(curr, prev.get(curr) + 1);
            } else {
                prev.set(curr, 1);
            }
            return prev;
        }, new Map());

    subs = subs.filter(([a, b]) => hashes.get(b) === 1);

    subs.sort(([a, b], [c, d]) => a - c);

    subs.map(([a, b]) => a).forEach((a) => console.log(a));
}
