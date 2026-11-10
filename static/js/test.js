series: [{
  data: DataAll,
  type: 'scatter',
  symbolSize: function(parmas) {
    return Math.ceil(parmas[2] / 1000);
  },
  label: {
    emphasis: {
      show: true,
      formatter: function(param) {
        return param.data[3] + param.data[4];
      },
      position: 'top',
    },
  },
  markLine: {
    data: [
      [{
          name: '标线1起点',
          xAxis: 0,
          yAxis: 300,
          symbol: 'circle'
        },
        {
          name: '标线1终点',
          xAxis: '2017年',
          yAxis: 300,
          symbol: 'circle'
        },
      ],
    ],
    label: {
      normal: {
        show: true,
        position: 'middle',
        formatter: '节能与新能源汽车技术路线图2020年目标',
      },
    },
    lineStyle: {
      normal: {
        type: 'solid',
        color: '#fff',
      },
    },
  },
  itemStyle: {
    normal: {
      color: '#0fefee',
    },
  },
}]