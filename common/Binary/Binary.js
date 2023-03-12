const { zip, product, sum, zipLongest } = require("../Collection/util");

class Binary {
    content;

    constructor(content) {
        if (Array.isArray(content) && content.length > 0) {
            this.content = content.slice();
            while (
                this.content.length > 1 &&
                this.content[this.content.length - 1] === 0
            ) {
                this.content.pop();
            }
        } else {
            this.content = [0];
        }
    }

    static from(iterable) {
        return new Binary([...iterable].map((n) => Number(n)).reverse());
    }

    static of(num) {
        const n = Math.trunc(Number(num));
        if (!Number.isSafeInteger(n) || n < 0) {
            throw new Error("You must provide a positive safe integer");
        }
        return Binary.from(n.toString(2));
    }

    or(...others) {
        return Binary.or_(this, ...others);
    }

    and(...others) {
        return Binary.and_(this, ...others);
    }

    xor(...others) {
        return Binary.xor_(this, ...others);
    }

    static or_(...binaries) {
        return new Binary(
            [...zipLongest(...binaries.map((bin) => bin.content), 0)].map(
                ([...vals]) => Math.max(...vals)
            )
        );
    }

    static and_(...binaries) {
        return new Binary(
            [...zipLongest(...binaries.map((bin) => bin.content), 0)].map(
                ([...vals]) => product(...vals)
            )
        );
    }

    static xor_(...binaries) {
        return new Binary(
            [...zipLongest(...binaries.map((bin) => bin.content), 0)].map(
                ([...vals]) => sum(...vals) % 2
            )
        );
    }

    toString() {
        return this.content.slice().reverse().join("");
    }
}

module.exports = Binary;
