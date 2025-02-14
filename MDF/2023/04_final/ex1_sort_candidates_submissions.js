input = [
    "5",
    "4 tropcourtpouretrevrai",
    "28 cac'estcool!",
    "3 tropcourtpouretrevrai",
    "30 un_poil_plus_long",
    "43 bondernier",
];
ContestResponse();

function ContestResponse() {
    console.error(input);

    let subs = input.slice(1).map((s) => s.split(" "));
    subs = subs.map(([a, b]) => [parseInt(a), b]);

    const hashes = subs
        .map(([a, b]) => b)
        .reduce((prev, curr) => {
            if (prev.has(curr)) {
                prev.set(curr, prev.get(curr) + 1);
            } else {
                prev.set(curr, 1);
            }
            return prev;
        }, new Map());

    subs = subs.filter(([a, b]) => hashes.get(b) === 1);

    subs.sort(([a, b], [c, d]) => a - c);

    subs.map(([a, b]) => a).forEach((a) => console.log(a));
}
