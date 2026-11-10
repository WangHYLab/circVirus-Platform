function plotVC() {
  var title = $('#tbody').children().eq(0).children().eq(1).text();
  var tableRowNum = $('#tbody').children().length;
  var nameList = [];
  var startList = [];
  var lengthList = [];
  var defaultColorList = [];
  var strandList = [];
  for (var i = 0; i < tableRowNum; i++) {
    var name = $('#tbody').children().eq(i).children().eq(0).text();
    var start = $('#tbody').children().eq(i).children().eq(4).text();
    var length = $('#tbody').children().eq(i).children().eq(6).text();
    var strand = $('#tbody').children().eq(i).children().eq(3).text();
    var virus = $('#tbody').children().eq(i).children().eq(1).text();
    if (title == virus) {
      if (name != 'NA') {
        nameList[nameList.length] = name;
        strandList[strandList.length] = strand;
        // console.log(nameList);
      };
      if (start != 'NA') {
        startList[startList.length] = start;
      };
      if (length != 'NA') {
        lengthList[lengthList.length] = length;
      };
      if (strand == '+') {
        defaultColorList[defaultColorList.length] = "#f7a35c";
      } else {
        defaultColorList[defaultColorList.length] = "#91c7ae";
      }
    };
  };
  // console.log(nameList);
  // console.log(startList);
  // console.log(lengthList);
  // var highPos = nameList.length * 40;
  if (nameList.length == 0) {
    $('#plot-all').height(0);
    $('#plot-all div').height(0);
    $('#plot-all canvas').height(0);
  } else if (nameList.length < 5) {
    $('#plot-all').height(120);
    $('#plot-all div').height(120);
    $('#plot-all canvas').height(120);
  } else if (nameList.length < 20 && nameList.length >= 5) {
    $('#plot-all').height(200);
    $('#plot-all div').height(200);
    $('#plot-all canvas').height(200);
  } else if (nameList.length < 50 && nameList.length >= 20) {
    $('#plot-all').height(300);
    $('#plot-all div').height(300);
    $('#plot-all canvas').height(300);
  } else if (nameList.length < 300 && nameList.length >= 50) {
    $('#plot-all').height(400);
    $('#plot-all div').height(400);
    $('#plot-all canvas').height(400);
  } else {
    $('#plot-all').height(600);
    $('#plot-all div').height(600);
    $('#plot-all canvas').height(600);
  }
  var plotTitle = 'virus-circRNA in '.concat(title);
  var plotSubtitle = 'Strand + : orange / Strand - : blue';
  // $('canvas').height(400);
  var myChart = echarts.init(document.getElementById('plot-all'));
  var option = {
    title: {
      text: plotTitle,
      subtext: plotSubtitle,
      // sublink: 'http://106.15.224.54/home/'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function(params) {
        var start = params[0];
        var tar = params[1];
        return 'name&nbsp&nbsp : ' + tar.name + '<br/>' + 'start&nbsp&nbsp&nbsp&nbsp : ' + start.value + '<br/>' + 'end&nbsp&nbsp&nbsp&nbsp&nbsp : ' + (parseInt(start.value) + parseInt(tar.value)).toString() + '<br/>' + tar.seriesName +
          ' &nbsp: ' + tar.value;
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    yAxis: {
      type: 'category',
      axisLabel: {
        fontSize: 9,
      },
      splitLine: {
        show: false
      },
      data: nameList
    },
    xAxis: {
      type: 'value',
      max: genomeLengh[title],

    },
    series: [{
        name: 'start',
        type: 'bar',
        stack: 'test',
        itemStyle: {
          barBorderColor: 'rgba(0,0,0,0)',
          color: 'rgba(0,0,0,0)'
        },
        emphasis: {
          itemStyle: {
            barBorderColor: 'rgba(0,0,0,0)',
            color: 'rgba(0,0,0,0)'
          }
        },
        data: startList
      },
      {
        name: 'length',
        type: 'bar',
        stack: 'test',
        label: {
          show: true,
          position: 'inside',
          formatter: 'text',
          textStyle: {
            color: 'red',
            fontSize: 8
          }
        },
        itemStyle: {
          normal: {
            color: function(params) {
              var colorList = defaultColorList;
              return colorList[params.dataIndex]
            }
          },
        },
        fontSize: 16,
        label: {
          show: false,
          position: 'inside',
        },
        data: lengthList
      },
    ],
    color: '#2f4f4f'
  };

  myChart.setOption(option);
  myChart.resize();
  myChart.on('click', function(series) {
    var id = series.name;
    var url = "/detail/?Circ_id=";
    var url = url.concat(id);
    window.location.href = url;
  });
};