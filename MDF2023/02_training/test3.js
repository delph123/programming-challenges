/*******
 * Read input from STDIN
 * Use: console.log()  to output your result.
 * Use: console.error() to output debug information into STDERR
 * ***/

var input = [];

readline_object.on("line", (value) => {
    //Read input values
    input.push(value);
});
//Call ContestResponse when all inputs are read
readline_object.on("close", ContestResponse);

function ContestResponse() {
    const N = parseInt(input[0]);
    const meet = input
        .slice(1)
        .map((others) => others.split(" ").map((n) => n === "1"));

    //   console.error(N, meet)

    //   const all = new Array(N)
    //     .fill(0)
    //     .map((_, i) => new Set(meet[i].map((_, j) => j).filter((j) => meet[i][j])));

    const all = [new Array(N).fill(0).map((_, i) => i)];

    //   console.error(meet);
    //   console.error(all);

    all.forEach((s) => {
        let stop = false;
        while (!stop) {
            let m = new Map();

            for (const val of s) {
                let nb = 0;
                for (const other of s) {
                    if (meet[val][other]) {
                        nb++;
                    }
                }
                m.set(val, nb);
            }

            const [wnei, wnb] = [...m.entries()].reduce(
                ([nei, nn], [mnei, mnn]) => {
                    if (nn < mnn) {
                        return [nei, nn];
                    } else {
                        return [mnei, mnn];
                    }
                },
                [-1, s.size + 1]
            );

            if (wnb < s.size) {
                s.delete(wnei);
            } else {
                stop = true;
            }
        }
    });

    console.error(all, Math.max(...all.map((s) => s.size)));
    console.log(Math.max(...all.map((s) => s.size)));
}
