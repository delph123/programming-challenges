const fs = require("fs");
const stdinBuffer = fs.readFileSync(0); // STDIN_FILENO = 0
const lines = stdinBuffer.toString().split("\r\n");

const seq = lines.map((i) => parseInt(i));

console.error("decrypting", seq);

const r = expand(
  mix(
    seq.map((n) => n * 811589153),
    10 * seq.length
  ),
  0
)
  .filter((v, i) => i === 1000 || i === 2000 || i === 3000)
  .reduce((a, b) => a + b, 0);

console.log("Key found:", r);

function mix(seq, N) {
  // Prepare
  let entries = seq.map((v, i) => ({ i, v }));
  entries.forEach((o, i, a) => {
    o.n = a[(i + 1) % entries.length];
    o.p = a[(i + entries.length - 1) % entries.length];
  });

  // Mix
  for (let i = 0; i < N; i++) {
    let e = entries[i % entries.length];
    let steps = e.v % (entries.length - 1);

    if (steps === 0) continue;

    // Remove from old position
    let a = e;
    let a1 = e.p;
    let a2 = e.n;
    a1.n = a2;
    a2.p = a1;

    // Search next position
    e = a1;
    for (let j = 0; j < Math.abs(steps); j++) {
      e = Math.sign(steps) > 0 ? e.n : e.p;
    }

    // Insert to new position
    let e2 = e.n;
    e.n = a;
    a.p = e;
    a.n = e2;
    e2.p = a;
  }

  return entries;
}

function expand(mix, from) {
  let r = [];
  let a = mix.find((v) => v.v === from);
  for (let i = 0; i < mix.length; i++) {
    r.push(a.v);
    a = a.n;
  }
  return r;
}
