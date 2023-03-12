const fs = require("fs");
const stdinBuffer = fs.readFileSync(0); // STDIN_FILENO = 0
const input = stdinBuffer.toString().split("\n");
input.pop();

ContestResponse();

function ContestResponse() {
    const [self, opponent] = input[0].split("-").map((n) => parseInt(n));

    if (self <= opponent) {
        console.log(Math.ceil((opponent + 1 - self) / 3));
    } else {
        console.log("0");
    }
}
