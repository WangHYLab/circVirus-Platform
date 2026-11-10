{
  var width = 500,
    height = 400;
  var cluster = d3.layout.tree()
    .size([width, height]);

  var diagonal = d3.svg.diagonal()
    .projection(function(d) {
      return [d.x, d.y];
    });
  var svg = d3.select("#tree2").append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("transform", "translate(" + 10 + "," + 50 + ")");
  // -----------------------------------------------------------------
  //箭头
  var marker =
    svg.append("marker")
    .attr("id", "resolved")
    .attr("markerUnits", "strokeWidth") //设置为strokeWidth箭头会随着线的粗细发生变化
    .attr("markerUnits", "userSpaceOnUse")
    .attr("viewBox", "0 -5 10 10") //坐标系的区域
    .attr("refX", 10) //箭头坐标
    .attr("refY", -1)
    .attr("markerWidth", 6) //标识的大小
    .attr("markerHeight", 6)
    .attr("orient", "auto") //绘制方向，可设定为：auto（自动确认方向）和 角度值
    .attr("stroke-width", 2) //箭头宽度
    .append("path")
    .attr("d", "M0,-5L10,0L0,5") //箭头的路径
    .attr('fill', 'grey'); //箭头颜色

  var treeData = '{{ conec_tree|safe }}';
  treeData = JSON.parse(treeData);
  var i = 0;
  var nodes = cluster.nodes(treeData).reverse();
  nodes.forEach(function(d) {
    d.y = d.depth * 50;
  });

  var links = cluster.links(nodes);
  var linkEnter = svg.selectAll("path.link")
    .data(links);

  linkEnter.enter().append("path") //在指定元素之前插入一个元素
    .attr("class", "link")
    .attr("d", diagonal)
    .attr("stroke", "white")
    .attr("marker-end", "url(#resolved)") //根据箭头标记的id号标记箭头
    .style("fill", "white")
    .style("fill-opacity", 1)
    // 首先为每条节点连线添加标识id
    .attr("id", function(d, i) {
      return "mypath" + i;
    });
  var node = svg.selectAll(".node")
    .data(nodes)
    .enter()
    .append("g")
    .attr("class", "node")
    .attr("transform", function(d) {
      return "translate(" + (d.x + -22) + "," + (d.y) + ")";
    })

  node.append("rect")
    // .attr("width", 44)
    .attr("width", function(d) {
      if (d.name[0] == "I") {
        return 100
      } else {
        return 44
      }
    })
    .attr("height", 30)
    .attr("x", function(d) {
      if (d.name[0] == "I") {
        return -25
      } else {
        return 0
      }
    })
    .attr("rx", function(d) {
      if (d.name[0] == "C") {
        return 22
      } else {
        return 8
      }
    })
    .attr("y", 0)
    .attr("fill", function(d) {
      if (d.name[0] == "C") {
        return "#2990ca"
      } else {
        return "grey"
      }
    })

  node.append("text")
    .attr("dx", function(d) {
      if (d.name[0] == "I") {
        return 25
      } else {
        return 22
      }
    })
    .attr("dy", 20)
    .style("text-anchor", function(d) {
      return "middle";
    })
    .style("fill", "#fff")
    .text(function(d) {
      return d.name;
    });

  node.on("click", function(d) {
      if (d.name != "") {
        // console.log(d.name);
        // console.log(d.name.split('C')[1]);
        piePlotNum = d.name.split('C')[1];
        piePlot(piePlotNum);
        // d3.select(this).attr("fill", "orange");
      }
    })
    .on("mouseover", function(d) {
      if (d.name != "") {
        d3.select(this).attr("style", "cursor:hand");
      }
    });
}