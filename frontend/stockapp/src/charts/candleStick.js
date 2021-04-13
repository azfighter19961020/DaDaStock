export function candleOption(sname,calculateMA,data){
  var upColor = '#ec0000'
  var upBorderColor = '#8A0000'
  var downColor = '#00da3c'
  var downBorderColor = '#008F28'
  return {
          title: {
             text: `${sname} \n K線圖`,
             left: 0
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
            type: 'cross'
            }
          },
          legend: {
            data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30'],
            left: 100
          },
          grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
          },
          xAxis: {
            type: 'category',
            data: data.categoryData,
            scale: true,
            boundaryGap: false,
            axisLine: {onZero: false},
            splitLine: {show: false},
            splitNumber: 20,
            min: 'dataMin',
          },
          yAxis: {
            scale: true,
            splitArea: {
            show: true
          }
        },
          dataZoom: [
            {
              type: 'inside',
              start: 50,
              end: 100
            },
            {
              show: true,
              type: 'slider',
              top: '90%',
              start: 50,
              end: 100
            }
          ],
          series: [
            {
              name: '日K',
              type: 'candlestick',
              data: data.values,
              itemStyle: {
                color: upColor,
                color0: downColor,
                borderColor: upBorderColor,
                borderColor0: downBorderColor
              },
              markPoint: {
                label: {
                    normal: {
                        formatter: function (param) {
                            return param != null ? Math.round(param.value) : '';
                        }
                    }
                },
                data: [
                    {
                        name: 'XX标点',
                        coord: ['2013/5/31', 2300],
                        value: 2300,
                        itemStyle: {
                            color: 'rgb(41,60,85)'
                        }
                    },
                    {
                        name: 'highest value',
                        type: 'max',
                        valueDim: 'highest'
                    },
                    {
                        name: 'lowest value',
                        type: 'min',
                        valueDim: 'lowest'
                    },
                    {
                        name: 'average value on close',
                        type: 'average',
                        valueDim: 'close'
                    },
                ],
                tooltip: {
                    formatter: function (param) {
                        return param.name + '<br>' + (param.data.coord || '');
                    }
                }
              },
              markLine: {
                symbol: ['none', 'none'],
                data: [
                    [
                        {
                            name: 'from lowest to highest',
                            type: 'min',
                            valueDim: 'lowest',
                            symbol: 'circle',
                            symbolSize: 10,
                            label: {
                                show: false
                            },
                            emphasis: {
                                label: {
                                    show: false
                                }
                            }
                        },
                        {
                            type: 'max',
                            valueDim: 'highest',
                            symbol: 'circle',
                            symbolSize: 10,
                            label: {
                                show: false
                            },
                            emphasis: {
                                label: {
                                    show: false
                                }
                            }
                        }
                    ],
                    {
                        name: 'min line on close',
                        type: 'min',
                        valueDim: 'close'
                    },
                    {
                        name: 'max line on close',
                        type: 'max',
                        valueDim: 'close'
                    }
                ]
                }
              },
              {
                        name: 'MA5',
                        type: 'line',
                        data: calculateMA(data,5),
                        smooth: true,
                        lineStyle: {
                        opacity: 0.5
                        }
              },
              {
                        name: 'MA10',
                        type: 'line',
                        data: calculateMA(data,10),
                        smooth: true,
                        lineStyle: {
                          opacity: 0.5
                        }
              },
              {
                        name: 'MA20',
                        type: 'line',
                        data: calculateMA(data,20),
                        smooth: true,
                        lineStyle: {
                          opacity: 0.5
                        }
            },
              {
                        name: 'MA30',
                        type: 'line',
                        data: calculateMA(data,30),
                        smooth: true,
                        lineStyle: {
                          opacity: 0.5
                        }
            },

          ]
        }
}

export function splitData(rawData) {
  var categoryData = []
  var values = []
  for (var i = 0; i < rawData.length; i++) {
    categoryData.push(rawData[i].splice(0, 1)[0])
    values.push(rawData[i])
  }
  return {
    categoryData: categoryData,
    values: values
  };
}

export function calculateMA(data,dayCount) {
  var result = [];
  for (var i = 0, len = data.values.length; i < len; i++) {
    if (i < dayCount) {
      result.push('-');
      continue;
    }
    var sum = 0;
    for (var j = 0; j < dayCount; j++) {
      sum += data.values[i - j][1];
    }
    result.push(sum / dayCount);
  }
  return result;
}