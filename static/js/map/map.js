let myChart = echarts.init(document.getElementById('china-map'));
let data = [
    {name: 'Beijing', value:33},
    {name: 'Shanghai', value:8},
    {name: 'Guangzhou', value:13},
    {name: 'Shenzhen', value:46},
];
let geoCoordMap = {
    'Guangzhou':[113.23, 23.16],
    'Shenzhen':[114.07, 22.62],
    'Beijing':[116.46, 39.92],
    'Shanghai':[121.47, 31.23]
};

let convertData = function (data) {
    let res = [];
    for (let i = 0; i < data.length; i++) {
        let geoCoord = geoCoordMap[data[i].name];
        if (geoCoord) {
            res.push({
                name: data[i].name,
                value: geoCoord.concat(data[i].value)
            });
        }
    }
    return res;
};

myChart.setOption(option = {
    title : {
        text: 'Departments location',
        left: 'center',
        top: 'top',
        textStyle: {
            color: '#fff'
        }
    },
    tooltip: {},
    legend: {
        left: 'left',
        data: [],
        textStyle: {
            color: '#ccc'
        }
    },
    backgroundColor: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 1,
        y2: 1,
        colorStops: [{
            offset: 0, color: '#0f2c70' // 0% 处的颜色
        }, {
            offset: 1, color: '#091732' // 100% 处的颜色
        }],
        globalCoord: false // 缺省为 false
    },
    geo: {
        map: 'china',
        show: true,
        roam: true,
        label: {
            emphasis: {
                show: false
            }
        },
        itemStyle: {
            normal: {
                areaColor: '#091632',
                borderColor: '#1773c3',
                shadowColor: '#1773c3',
                shadowBlur: 20
            }
        }
    },
    series: [
        {
            type: 'map',
            map: 'china',
            geoIndex: 1,
            aspectScale: 0.75, //长宽比
            showLegendSymbol: true, // 存在legend时显示
            label: {
                normal: {
                    show: false,
                },
                emphasis: {
                    show: false,
                    textStyle: {
                        color: '#fff'
                    }
                }
            },
            roam: true,
            itemStyle: {
                normal: {
                    areaColor: '#031525',
                    borderColor: '#3B5077',
                    borderWidth: 1
                },
                emphasis: {
                    areaColor: '#0f2c70'
                }
            },
            data:[
                // {name: '北京',value: 21300 }
            ]
        },
        {
            name: 'city',
            type: 'scatter',
            coordinateSystem: 'geo',
            data: convertData(data),
            symbolSize: function (val) {
                return val[2];
            },
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: false
                },
                emphasis: {
                    show: true
                }
            },
            itemStyle: {
                normal: {
                    color: '#ddb926'
                }
            }
        },
        {
            name: 'location',
            type: 'effectScatter',
            coordinateSystem: 'geo',
            data: convertData(data.sort(function (a, b) {
                return b.value - a.value;
            }).slice(0, 6)),
            symbolSize: function (val) {
                return val[2];
            },
            showEffectOn: 'render',
            rippleEffect: {
                brushType: 'stroke'
            },
            hoverAnimation: true,
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: true
                }
            },
            itemStyle: {
                normal: {
                    color: '#f4e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            zlevel: 1
        }
    ]
});