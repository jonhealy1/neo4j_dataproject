import React, {Component} from 'react'
import ChordDiagram from 'react-chord-diagram'


// export class Chord extends Component {

//     render() {
//         const matrix = [
//             [11975, 5871, 8916, 2868],
//             [1951, 10048, 2060, 6171],
//             [8010, 16145, 8090, 8045],
//             [1013, 990, 940, 6907]
//         ];
//         return(
//             <ChordDiagram
//                 width={800}
//                 height={800}
//                 disableHover = {true}
//                 disableRibbonHover = {false}
//                 matrix={matrix}
//                 componentId={1}
//                 groupLabels={['Black', 'Yellow', 'Brown', 'Orange']}
//                 groupColors={["#000000", "#FFDD89", "#957244", "#F26223"]}
//             />
//         )
//     }
// }

export class Chord extends Component {

    render() {
        const matrix = [
            [0, 16, 17, 24, 17, 35, 11, 26, 22],
            [17, 0, 0, 1, 0, 1, 0, 3, 12],
            [10, 0, 0, 2, 0, 25, 10, 2, 1],
            [5, 0, 1, 0, 1, 6, 0, 0, 0],
            [9, 0, 0, 6, 0, 2, 0, 1, 1],
            [38, 3, 13, 75, 3, 0, 10, 8, 5],
            [11, 0, 7, 0, 0 , 7, 0, 6, 0],
            [32, 12, 7, 2, 0, 13, 11, 0, 1],
            [17, 5, 1, 6, 1, 16, 1, 3, 0]
        ];
        return(
            <ChordDiagram
                width={800}
                height={800}
                disableHover = {true}
                disableRibbonHover = {false}
                matrix={matrix}
                componentId={1}
                groupLabels={['the_donald', 'hillaryclinton', 'wikileaks', 'worldnews', 'conservative', 'conspiracy', 'dncleaks', 'hillaryforprison', 'enoughtrumpspam']}
                groupColors={["violet", "green", "orange", "yellow", "blue", "red", "indigo", "black", "grey"]}
                //groupColors={["#619242", "#67A144", "#6EB045", "#C34E8D", "#C5506E", "#C65451", "#375F1B", "#C87753", "#9EE3635"]}
            />
        )
    }
}
