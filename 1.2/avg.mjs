// Importing required RxJS operators
import { from } from 'rxjs';
import { filter, map, mergeMap, reduce } from 'rxjs/operators';

// Sample data
let persons = [
    { id: 1, name: "Jan Kowalski" },
    { id: 2, name: "John Doe" },
    { id: 3, name: "Jarek Kaczka" }
];

let ages = [
    { person: 1, age: 18 },
    { person: 2, age: 24 },
    { person: 3, age: 666 }
];

let locations = [
    { person: 1, country: "Poland" },
    { person: 3, country: "Poland" },
    { person: 1, country: "USA" }
];



from(locations).pipe(
    filter(location => location.country === 'Poland'),

    mergeMap(location => from(ages).pipe(
        filter(age => age.person === location.person),
        map(age => age.age)
    )),

    reduce((acc, age) => {
        acc.sum += age;
        acc.count++;
        return acc;
    }, { sum: 0, count: 0 }),
    map(acc => acc.count > 0 ? acc.sum / acc.count : 0)
).subscribe(avgAge => {
    console.log(`Średni wiek osób z Polski: ${avgAge}`);
});