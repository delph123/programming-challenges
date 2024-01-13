const { part_one, part_two, read, sum } = require("../../common/aoc");

const commands = read("example")
    .split("$ ")
    .slice(1)
    .map((c) => c.split("\n").filter((s) => s.length > 0));

part_one(
    sum(
        walkFs(runScript(commands))
            .map((m) => m.get("$_size_$"))
            .filter((s) => s < 100000)
    )
);

const minFreeSize = runScript(commands).get("$_size_$") - 40000000;
const bigEnough = walkFs(runScript(commands))
    .map((m) => m.get("$_size_$"))
    .filter((s) => s >= minFreeSize)
    .sort((a, b) => a - b);

part_two(Math.min(...bigEnough));

function walkFs(fs) {
    let subs = [...fs.entries()]
        .filter(([d]) => !d.startsWith("$_") && d !== "..")
        .map(([_, sfs]) => walkFs(sfs));
    return [...[].concat(...subs), fs];
}

function computeSize(fs) {
    fs.forEach((v, k) => {
        if (!k.startsWith("$_") && k !== "..") {
            computeSize(fs.get(k));
        }
    });
    fs.set(
        "$_filesize_$",
        [...fs.get("$_files_$").entries()].reduce(
            (sum, [f, size]) => sum + size,
            0
        )
    );
    fs.set(
        "$_size_$",
        [...fs.entries()]
            .filter(([d]) => !d.startsWith("$_") && d !== "..")
            .reduce((sum, [_, sfs]) => sfs.get("$_size_$") + sum, 0) +
            fs.get("$_filesize_$")
    );
}

function runScript(commands) {
    let fs = dir();
    commands.reduce((fs, cmd) => {
        if (cmd[0] === "ls") {
            return ls(fs, cmd);
        } else {
            return cd(fs, cmd[0]);
        }
    }, new Map([["/", fs]]));
    computeSize(fs);
    return fs;
}

function dir(parent) {
    return new Map([
        ["$_files_$", new Map()],
        ["..", parent],
    ]);
}

function ls(fs, list) {
    list.slice(1).forEach((l) => {
        let [a, b] = l.split(" ");
        if (a === "dir") {
            fs.set(b, dir(fs));
        } else {
            fs.get("$_files_$").set(b, parseInt(a));
        }
    });
    return fs;
}

function cd(fs, cmd) {
    return fs.get(cmd.split(" ")[1]);
}
