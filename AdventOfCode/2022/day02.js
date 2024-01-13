const { sum, readLines, part_one, part_two } = require("../../common/aoc");

const guide = readLines("example").map((line) => line.split(" "));

const SHAPE_SCORE = { X: 1, Y: 2, Z: 3 };
const OUTCOME_SCORE = {
    AX: 3,
    BY: 3,
    CZ: 3,
    AY: 6,
    BZ: 6,
    CX: 6,
    AZ: 0,
    BX: 0,
    CY: 0,
};

const scores = guide.map(([o, m]) => OUTCOME_SCORE[o + m] + SHAPE_SCORE[m]);

part_one(sum(scores));

const CHOICE = {
    AY: "X",
    BY: "Y",
    CY: "Z",
    AZ: "Y",
    BZ: "Z",
    CZ: "X",
    AX: "Z",
    BX: "X",
    CX: "Y",
};

const scores_p2 = guide.map(
    ([o, m]) => OUTCOME_SCORE[o + CHOICE[o + m]] + SHAPE_SCORE[CHOICE[o + m]]
);

part_two(sum(scores_p2));
