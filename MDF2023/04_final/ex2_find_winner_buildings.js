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
    console.error(input);

    const [n, m, t] = input[0].split(" ").map((n) => parseInt(n));
    const cheats = input[1].split(" ").map((n) => parseInt(n));
    const roads = input
        .slice(2)
        .map((r) => r.split(" ").map((n) => parseInt(n)));

    const edges = new Map();
    for (let i = 0; i <= n; i++) {
        edges.set(i, new Set());
    }
    roads.forEach(([a, b]) => {
        let nb = edges.get(a).add(b);
        edges.set(a, nb);
        let na = edges.get(b).add(a);
        edges.set(b, na);
    });

    // console.error(n, m, t);
    // console.error(cheats);
    // console.error(roads);

    const winner = new Set([1]);
    let cheaters = new Set(cheats);
    let oldCheaters = new Set(cheaters);

    const remain = new Set(new Array(n).fill(0).map((_, i) => i));
    remain.delete(1);
    cheaters.forEach((p) => {
        remain.delete(p);
    });

    console.error(winner, cheaters, remain);

    while (remain.size > 0) {
        let s = remain.size;
        const c = [...cheaters];

        cheaters = new Set();
        c.forEach((p) => {
            // console.error("Found", p, edges.get(p));
            [...edges.get(p)].forEach((nei) => {
                cheaters.add(nei);
                remain.delete(nei);
            });
        });

        cheaters.forEach((p) => {
            oldCheaters.add(p);
        });

        const d = [...winner];
        d.forEach((p) => {
            // console.error("Found2", p, edges.get(p));
            [...edges.get(p)].forEach((nei) => {
                if (!oldCheaters.has(nei)) {
                    winner.add(nei);
                    remain.delete(nei);
                }
            });
        });
        // console.error("Next", remain);
        if (s === remain.size) {
            break;
        }
    }

    console.log([...winner].sort((a, b) => a - b).join(" "));
}
