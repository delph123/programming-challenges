function randomInt(max) {
    return Math.floor(Math.random() * max);
}

const generatedIds = new Map();

function getNextId(scope = "global", max = 1_000_000) {
    if (!generatedIds.has(scope)) {
        generatedIds.set(scope, []);
    }

    const ids = generatedIds.get(scope);

    let retries = 10;
    while (retries > 0) {
        retries--;
        const i = randomInt(max);
        if (!ids.includes(i)) {
            ids.push(i);
            return i;
        }
    }

    throw new Error(`No more ID available for scope ${scope}`);
}

module.exports = {
    randomInt,
    getNextId,
};
