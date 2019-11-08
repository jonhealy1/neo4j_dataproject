import * as d3 from 'd3';
import React, {Component} from 'react';



import './adjacency_matrix.style.css'

export class AdjacencyMatrix extends Component {


    render_adjacency_matrix = (data) => {
        let miserables = data;
        let margin = {top: 80, right: 0, bottom: 10, left: 80},
            width = 720,
            height = 720;

        miserables.links.forEach(link => {
            for(let i = 0; i < miserables.nodes.length; i++) {
                if(miserables.nodes[i].name === link.source) {
                    link.source = miserables.nodes[i].index;
                }
                if(miserables.nodes[i].name === link.target) {
                    link.target = miserables.nodes[i].index;
                }
            }
        })
        miserables.nodes.forEach(node => {
            node.group = Math.floor(Math.abs(Math.log(node.group)));
        })

        let x = d3.scaleBand().range([0, width]),
            z = d3.scaleLinear().domain([0, 4]).clamp(true),
            c = d3.schemeCategory10;

        let svg = d3.select(this.ref).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .style("margin-left", -margin.left + "px")
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        let matrix = [],
            nodes = miserables.nodes,
            n = nodes.length;

        nodes.forEach(function(node, i) {
            node.index = i;
            node.count = 0;
            matrix[i] = d3.range(n).map(function(j) { return {x: j, y: i, z: 0}; });
        });

        miserables.links.forEach(function(link) {
            matrix[link.source][link.target].z += link.value;
            matrix[link.target][link.source].z += link.value;
            matrix[link.source][link.source].z += link.value;
            matrix[link.target][link.target].z += link.value;
            nodes[link.source].count += link.value;
            nodes[link.target].count += link.value;
        });

        let orders = {
            name: d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].name, nodes[b].name); }),
            count: d3.range(n).sort(function(a, b) { return nodes[b].count - nodes[a].count; }),
            group: d3.range(n).sort(function(a, b) { return nodes[b].group - nodes[a].group; })
        };

        // The default sort order.
        x.domain(orders.name);

        svg.append("rect")
            .attr("class", "background")
            .attr("width", width)
            .attr("height", height);

        let row = svg.selectAll(".row")
            .data(matrix)
            .enter().append("g")
            .attr("class", "row")
            .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
            .each(row_function);

        row.append("line")
            .attr("x2", width);

        row.append("text")
            .attr("x", -6)
            .attr("y", x.bandwidth() / 2)
            .attr("dy", ".32em")
            .attr("text-anchor", "end")
            .text(function(d, i) { return nodes[i].name; });

        let column = svg.selectAll(".column")
            .data(matrix)
            .enter().append("g")
            .attr("class", "column")
            .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

        column.append("line")
            .attr("x1", -width);

        column.append("text")
            .attr("x", 6)
            .attr("y", x.bandwidth() / 2)
            .attr("dy", ".32em")
            .attr("text-anchor", "start")
            .text(function(d, i) { return nodes[i].name; });

        function row_function(row) {
             d3.select(this).selectAll(".cell")
                .data(row.filter(function(d) { return d.z; }))
                .enter().append("rect")
                .attr("class", "cell")
                .attr("x", function(d) { return x(d.x); })
                .attr("width", x.bandwidth())
                .attr("height", x.bandwidth())
                .style("fill-opacity", function(d) { return z(d.z); })
                .style("fill", function(d) {
                    return nodes[d.x].group === nodes[d.y].group ? c[nodes[d.x].group] : null; })
                .on("mouseover", mouseover)
                .on("mouseout", mouseout);
        }

        function mouseover(p) {
            d3.selectAll(".row text").classed("active", function(d, i) { return i === p.y; });
            d3.selectAll(".column text").classed("active", function(d, i) { return i === p.x; });
        }

        function mouseout() {
            d3.selectAll("text").classed("active", false);
        }


        d3.select("#order").on("change", function() {
            clearTimeout(timeout);
            order(this.value);
        });

        function order(value) {
            x.domain(orders[value]);

            var t = svg.transition().duration(2500);

            t.selectAll(".row")
                .delay(function(d, i) { return x(i) * 4; })
                .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
                .selectAll(".cell")
                .delay(function(d) { return x(d.x) * 4; })
                .attr("x", function(d) { return x(d.x); });

            t.selectAll(".column")
                .delay(function(d, i) { return x(i) * 4; })
                .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });
        }

        var timeout = setTimeout(function() {
            order("group");
            d3.select("#order").property("selectedIndex", 2).node().focus();
        }, 5000);


    }
    componentDidMount() {
        fetch(`${this.props.ip}/adjacency-matrix`)
            .then(result => (result.json()))
            .then(data => {
                this.render_adjacency_matrix(data);
            })

    }

    render() {
        return(
            <div>
                <p>Change order by selecting a category: <select id="order">
                    <option value="name">by Name</option>
                    <option value="count">by Frequency</option>
                    <option value="group">by Cluster</option>
                </select>
                </p>
            <svg className={'adjacency-matrix'} ref={(ref) => this.ref = ref} width={1000} height={1000}>
            </svg>
            </div>
        )
    }
}
