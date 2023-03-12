const fs = require("fs");
const stdinBuffer = fs.readFileSync(0); // STDIN_FILENO = 0
const input = stdinBuffer.toString().split("\n");
input.pop();

ContestResponse();

function ContestResponse() {
    console.error(input);
    const field = input.slice(1).map((l) => l.split(""));

    let found = false;

    for (let i = 0; i < field.length - 1; i++) {
        for (let j = 0; j < field[i].length - 1; j++) {
            if (canCreateGarden(field, i, j)) {
                found = true;
                field[i][j] = "O";
                field[i][j + 1] = "O";
                field[i + 1][j] = "O";
                field[i + 1][j + 1] = "O";
                break;
            }
        }
        if (found) {
            break;
        }
    }

    if (found) {
        field.forEach((l) => console.log(l.join("")));
    } else {
        console.log("Impossible");
    }
}

function canCreateGarden(field, i, j) {
    return (
        field[i][j] === "." &&
        field[i][j + 1] === "." &&
        field[i + 1][j] === "." &&
        field[i + 1][j + 1] === "."
    );
}
