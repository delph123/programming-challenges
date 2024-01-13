const path = require("path");
const fs = require("fs");

function read(version) {
    // Read file name from main script
    const calling_path = path.parse(require.main.filename);
    const year = path.basename(calling_path.dir);
    const day = calling_path.name.substring(3);

    console.log(
        `\x1b[30;35m--- Advent of Code ${year} - Day ${day} ---\x1b[0m`
    );

    let directory = "inputs";

    if (version.startsWith("e")) {
        console.log("\x1b[30;41m /!\\ \x1b[0m Reading from example");
        directory = "examples";
    }

    return fs
        .readFileSync(
            path.join(calling_path.dir, directory, `day${day}.in`),
            "utf-8"
        )
        .replaceAll("\r", "")
        .trim();
}

function readLines(version) {
    return read(version).split("\n");
}

module.exports = {
    read,
    readLines,
};
