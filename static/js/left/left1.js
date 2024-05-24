document.addEventListener('DOMContentLoaded', function () {
            // 使用 fetch 从后端获取数据
            // 替换 '/your-backend-endpoint' 为实际的后端端点
            fetch('/relation_PhysicalDefense_PhysicalDamageReduction')
                .then(response => response.json())
                .then(data => {
                    // 处理 JSON 数据为 ECharts 所需格式
                    let processedData = processData_l1(data);
                    console.log(processedData);
                    // 使用 ECharts 创建堆叠面积图
                    createStackedAreaChart_l1(processedData);
                })
                .catch(error => console.error('Error fetching data:', error));
        });

        // 处理 JSON 数据为 ECharts 所需格式
function processData_l1(data) {
    let processedData = {
        positions: [],
        physicalDefense: [],
        physicalDamageReduction: []
    };

    for (let i = 0; i < data.length; i++) {
        processedData.positions.push(data[i].Position);
        processedData.physicalDefense.push(data[i].PhysicalDefense);
        processedData.physicalDamageReduction.push(data[i].PhysicalDamageReduction);
    }

    return processedData;
}

// 使用 ECharts 创建堆叠面积图
function createStackedAreaChart_l1(data) {
    let chartContainer = document.getElementById('left1');
    let myChart = echarts.init(chartContainer);

    let option = {
        title: {
            text: 'PhysicalDefense and Physical Damage Reduction by Position',
            left: 'center',
            textStyle: {
                fontSize: 12 // 设置字体大小
            },
            top: 5
        },
        legend: {
            data: ['Physical Defense', 'Physical Damage Reduction'],
            top: 25
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: data.positions,
            axisLabel: {
                interval: 0, // 全部显示标签
                rotate: 45, // 旋转角度，可以根据需要调整
                textStyle: {
                    fontSize: 10 // 标签字体大小
                }
            },
            axisTick: {
                show: false
            },
            axisLine: {
                show: false
            },
            z: 10
        },
        yAxis: {
            type: 'value',
            axisLine: {
                show: false
            },
            axisTick: {
                show: false
            },
            axisLabel: {
                color: '#999'
            }
        },
        series: [
            {
                name: 'Physical Defense',
                type: 'line', // 堆叠面积图的类型为线
                stack: 'total',
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: data.physicalDamageReduction
            },
            {
                name: 'Physical Damage Reduction',
                type: 'line', // 堆叠面积图的类型为线
                stack: 'total',
                areaStyle: {},
                emphasis: {
                    focus: 'series'
                },
                data: data.physicalDefense
            }
        ],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            },
            formatter: function (params) {
                let tooltip = params[0].name + '<br>';
                for (let i = 0; i < params.length; i++) {
                    tooltip += params[i].seriesName + ': ' + params[i].value + '<br>';
                }
                return tooltip;
            }
        }
    };

    myChart.setOption(option);
}