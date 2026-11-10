// , colorList, data, dataSubtype
var createdivMut = function(id) {
  var parentdiv = $('.right-plot'); //创建一个父div
  var childdiv = $('<div></div>'); //创建一个子div
  childdiv.attr('id', id); //给子div设置id
  childdiv.addClass('bar-plot-mut'); //添加css样式
  childdiv.appendTo(parentdiv); //将子div添加到父div中
};

function barplotMut(plotBixId, colorList, barData) {
  createdivMut(plotBixId);
  var colName = [];

  for (var i = 0; i < barData.length; i++) {
    colName[i] = 'C'.concat(i + 1);
  }
  var domBar = document.getElementById(plotBixId);
  var barChart = echarts.init(domBar);
  optionBar = {
    title: {
      text: plotBixId,
      x: 'center',
      textStyle: {
        fontSize: 13,
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [{
      type: 'category',
      data: colName,


      axisTick: {
        alignWithLabel: true
      }
    }],
    yAxis: [{
      type: 'value',
      name: 'mut prop'
    }],
    series: [{
      // name: '直接访问',
      type: 'bar',
      barWidth: '60%',
      data: barData,
      itemStyle: {
        // barBorderRadius: 6,
        //每根柱子颜色设置
        color: function(params) {
          return colorList[params.dataIndex];
        }
      },
    }]
  };
  barChart.setOption(optionBar, true);
};
// , colorList, data, dataSubtype
var createdivExpr = function(id) {
  var parentdiv = $('.right-plot'); //创建一个父div
  var childdiv = $('<div></div>'); //创建一个子div
  childdiv.attr('id', id); //给子div设置id
  childdiv.addClass('bar-plot-expr'); //添加css样式
  childdiv.appendTo(parentdiv); //将子div添加到父div中
};

function barplotExpr(plotBixId, colorList, barData) {
  createdivExpr(plotBixId);
  // console.log(plotBixId);
  // console.log(colorList);
  // console.log(barData);
  var colName = [];
  for (var i = 0; i < barData.length; i++) {
    colName[i] = 'C'.concat(i + 1);
  }
  var domBar = document.getElementById(plotBixId);
  var barChart = echarts.init(domBar);
  optionBar = {
    title: {
      text: plotBixId,
      x: 'center',
      textStyle: {
        fontSize: 13,
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [{
      type: 'category',
      data: colName,


      axisTick: {
        alignWithLabel: true
      }
    }],
    yAxis: [{
      type: 'value',
      name: 'expr'
    }],
    series: [{
      // name: '直接访问',
      type: 'bar',
      barWidth: '60%',
      data: barData,
      itemStyle: {
        // barBorderRadius: 6,
        //每根柱子颜色设置
        color: function(params) {
          return colorList[params.dataIndex];
        }
      },
    }]
  };
  barChart.setOption(optionBar, true);
};