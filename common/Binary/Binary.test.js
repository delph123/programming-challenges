const Binary = require("./Binary");

describe("Binary construction", () => {
    it("Creates a new empty Binary object", () => {
        expect(new Binary().toString()).toEqual("0");
        expect(Binary.from("").toString()).toEqual("0");
        expect(Binary.of(0).toString()).toEqual("0");
    });

    it("Creates a new Binary object", () => {
        expect(new Binary([1, 0, 1, 1]).toString()).toEqual("1101");
        expect(new Binary([1, 1, 0, 0]).toString()).toEqual("11");
        expect(new Binary([0, 0, 0, 0]).toString()).toEqual("0");
    });

    it("Creates a new Binary object from a string", () => {
        expect(Binary.from("0").toString()).toEqual("0");
        expect(Binary.from("10001011").toString()).toEqual("10001011");
        expect(Binary.from("001").toString()).toEqual("1");
    });

    it("Creates a new Binary object from a number", () => {
        expect(Binary.of(0b0).toString()).toEqual("0");
        expect(Binary.of(0b11001).toString()).toEqual("11001");
        expect(Binary.of(0b001).toString()).toEqual("1");
        expect(Binary.of(0b1111).toString()).toEqual("1111");
    });
});

describe("Binary operations", () => {
    it("Computes binary or", () => {
        expect(Binary.from("10011").or().toString()).toEqual("10011");
        expect(Binary.from("10011").or(Binary.from("100")).toString()).toEqual(
            "10111"
        );
        expect(
            Binary.from("10011")
                .or(Binary.from("100"), Binary.from("0"), Binary.from("1010"))
                .toString()
        ).toEqual("11111");
    });

    it("Computes binary xor", () => {
        expect(Binary.from("10011").xor().toString()).toEqual("10011");
        expect(Binary.from("10011").xor(Binary.from("101")).toString()).toEqual(
            "10110"
        );
        expect(
            Binary.from("10011")
                .xor(Binary.from("100"), Binary.from("0"), Binary.from("1010"))
                .toString()
        ).toEqual("11101");
    });

    it("Computes binary and", () => {
        expect(Binary.from("10011").and().toString()).toEqual("10011");
        expect(Binary.from("10011").and(Binary.from("100")).toString()).toEqual(
            "0"
        );
        expect(
            Binary.from("10011")
                .and(Binary.from("111"), Binary.from("10"), Binary.from("1010"))
                .toString()
        ).toEqual("10");
    });
});
