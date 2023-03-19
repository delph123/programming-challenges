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
    const meet = input
        .slice(1)
        .map((others) => others.split(" ").map((n) => n === "1"));

    const participants = new Set(
        new Array(meet.length).fill(0).map((_, i) => i)
    );

    while (true) {
        let candidate = -1;
        let min_neighbours = participants.size + 1;

        for (const neighbour of participants) {
            let nb = 0;
            for (const other of participants) {
                if (meet[neighbour][other]) {
                    nb++;
                }
            }
            if (nb < min_neighbours) {
                candidate = neighbour;
                min_neighbours = nb;
            }
        }

        if (min_neighbours < participants.size) {
            participants.delete(candidate);
        } else {
            break;
        }
    }

    // console.error(all, all.size);
    console.log(participants.size);
}
