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

    const points = { J: 0, R: 0 };

    for (let j = 0; j < input.length; j++) {
        let who = "";
        let nb = 0;
        for (let i = 0; i < input[j].length; i++) {
            if (input[j][i] === who) {
                nb++;
            } else {
                if (nb > 3) {
                    points[who] += nb - 3;
                }
                who = input[j][i];
                nb = 1;
            }
        }
        if (nb > 3) {
            points[who] += nb - 3;
        }
    }

    console.error(points);

    for (let i = 0; i < input[0].length; i++) {
        let who = "";
        let nb = 0;
        for (let j = 0; j < input.length; j++) {
            if (input[j][i] === who) {
                nb++;
            } else {
                if (nb > 3) {
                    points[who] += nb - 3;
                }
                who = input[j][i];
                nb = 1;
            }
        }
        if (nb > 3) {
            points[who] += nb - 3;
        }
    }

    console.error(points);

    if (points.R > points.J) {
        console.log("R");
    } else if (points.J > points.R) {
        console.log("J");
    } else {
        console.log("NOBODY");
    }
}
