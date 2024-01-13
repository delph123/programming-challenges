const readers = require("./reader");
const collection_utils = require("../Collection/util");

function print_result(result, part) {
    console.log(`\x1b[30;${part == 1 ? 36 : 32}mPart ${part}:\x1b[0m`, result);
}

function part_one(result) {
    print_result(result, 1);
}

function part_two(result) {
    print_result(result, 2);
}

module.exports = {
    part_one,
    part_two,
    ...readers,
    ...collection_utils,
};
