const { part_one, part_two, read } = require("../../common/aoc");

const packets = [...read("example")];

function findFirstDistinctPacket(packets, packetSize) {
    let firstIndex = packets.findIndex((_, i) =>
        i < packetSize - 1
            ? false
            : new Set(
                  new Array(packetSize).fill(0).map((_, j) => packets[i - j])
              ).size === packetSize
    );
    return firstIndex + 1;
}

part_one(findFirstDistinctPacket(packets, 4));
part_two(findFirstDistinctPacket(packets, 14));
