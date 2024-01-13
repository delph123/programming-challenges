const { read, sum, part_one, part_two } = require("../../common/aoc");

const elvesCalories = read("example")
    .split("\n\n") // split per elf
    .map((a) => a.split("\n").map((i) => parseInt(i))) // split inventory items
    .map((a) => sum(a)) // sum calories per elf
    .sort((a, b) => b - a);

part_one(elvesCalories[0]);

part_two(sum(elvesCalories.slice(0, 3)));
