const lines = [
  "9534180267 ____|||_|__|||__|_|_|_|_|||||_|___||_",
  "4973152608 _|||____||__|___|_||||||_|___|_|||_|_",
  "276913717211",
];

const [raw1, crypt1] = lines[0].split(" ");
const [raw2, crypt2] = lines[1].split(" ");
const tbd = lines[2];
const [nb1, nb2] = [[...raw1], [...raw2]];

const nbs_crypt = decrypt(new Map(), nb1, nb2, crypt1, crypt2);
console.log(nbs_crypt);

console.log(encrypt(nbs_crypt, [...tbd]));

function encrypt(crypt_map, rawNbs) {
  return "".concat(...rawNbs.map((n) => crypt_map.get(n)));
}

function decrypt(crypt_map, nb1, nb2, crypt1, crypt2) {
  if (crypt1.length === 4 * nb1.length) {
    // eat all
    nb1.forEach((n, i) => {
      crypt_map.set(n, crypt1.substring(i * 4, 4 * (i + 1)));
    });

    // check & return
    if (encrypt(crypt_map, nb2) === crypt2) {
      return crypt_map;
    } else {
      return null;
    }
  }

  const [n, ...rest] = nb1;

  // pick 3
  const map3 = decrypt(
    add(crypt_map, n, crypt1.substring(0, 3)),
    rest,
    nb2,
    crypt1.substring(3),
    crypt2
  );
  if (map3 !== null) {
    return map3;
  }

  // pick 4
  return decrypt(
    add(crypt_map, n, crypt1.substring(0, 4)),
    rest,
    nb2,
    crypt1.substring(4),
    crypt2
  );
}

function add(map, n, str) {
  return new Map([...map.entries()]).set(n, str);
}
