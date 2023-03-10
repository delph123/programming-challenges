const fs = require("fs");
const stdinBuffer = fs.readFileSync(0); // STDIN_FILENO = 0
const input = stdinBuffer.toString().split("\n");
input.pop();

ContestResponse();

function ContestResponse() {
    console.error(input);
}
