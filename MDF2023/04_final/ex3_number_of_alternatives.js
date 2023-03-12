const input = [
    "10",
    "1 marketing computers",
    "2 dancing dancing",
    "3 computers customer_relationship",
    "4 music entertainment",
    "5 bread sausages",
    "6 computers journalism",
    "7 advertising web_scrapping",
    "8 dancing video",
    "9 books children_books",
    "10 cars electric_cars",
];

let business;

ContestResponse();

function ContestResponse() {
    business = input.slice(1).map((line) => line.split(" "));

    console.log(count(business.length - 1, new Set()));
}

function count(idx, exn) {
    const [, a, b] = business[idx];

    if (exn.has(a) && exn.has(b)) {
        return 0;
    } else if (exn.has(a)) {
        if (idx === 0) {
            return 1;
        } else {
            return count(idx - 1, new Set([...exn, a]));
        }
    } else if (exn.has(b)) {
        if (idx === 0) {
            return 1;
        } else {
            return count(idx - 1, new Set([...exn, b]));
        }
    } else {
        if (idx === 0) {
            return 2;
        } else {
            return (
                count(idx - 1, new Set([...exn, a])) +
                count(idx - 1, new Set([...exn, b]))
            );
        }
    }
}
