import React, {Component} from 'react';
import './App.css';

import {Chord} from "./components/chord.diagram.component";
import {EdgeBundled} from "./components/edge_bundled.diagram.component";
import {NodeLink} from "./components/NodeLink.component";
import {AdjacencyMatrix} from "./components/adjacency_matrix.diagram.component";

class App extends Component{
    constructor(props){
        super(props);

        this.state = {
            localIP: 'http://127.0.0.1:5000',
        }
    }
    render() {
        return (
            <div className="App">
                <h2 className={'margin-top-100'}>Chord diagram</h2>
                <Chord/>
                <h2 className={'margin-top-100'}>Edge Bundling diagram</h2>
                <p><span className={'red'}>Red</span> is outgoing edges and <span className={'green'}>green</span> is ingoing</p>
                <p>Nodes close to each other are in a group</p>
                <p className={'margin-top-100'}>50 nodes</p>
                <EdgeBundled size={50} ip={this.state.localIP}/>
                <p>100 nodes</p>
                <EdgeBundled size={100} ip={this.state.localIP}/>

                <h2 className={'margin-top-100'}>Node-Link diagram</h2>
                <p className={'margin-top-100'}>6 nodes</p>
                <NodeLink size={6} ip={this.state.localIP}/>
                <p>20 nodes</p>
                <NodeLink size={20} ip={this.state.localIP}/>
                <h2 className={'margin-top-100'}>Adjacency Matrix diagram </h2>
                <p>Different colors show different groups and different opacity show edge weights in that group</p>
                <AdjacencyMatrix ip={this.state.localIP}/>
                <div className={'margin-bottom-100'}></div>
            </div>
        );
    }
}

export default App;
