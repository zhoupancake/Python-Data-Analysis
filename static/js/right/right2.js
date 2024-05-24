document.addEventListener('DOMContentLoaded', function () {
    // 使用 fetch 从后端获取数据
    // 替换 '/your-backend-endpoint' 为实际的后端端点
    fetch('/distribution_health_each_position')
        .then(response => response.json())
        .then(data => {
            let processedData = processData_r2(data);
            createBoxplot_r2(processedData);
        })
        .catch(error => console.error('Error fetching data:', error));
});

// 处理 JSON 数据为 ECharts 所需格式
function processData_r2(data) {
    let categories = ['0'].concat(data[0]);
    let values = ['0'];
    for(let i = 0; i < data[0].length; i++)
        values.push(calculateBoxplotValues_r2(data[1][i]));
    return {
        categories: categories,
        values: values
    };
}

function calculateBoxplotValues_r2(data) {
    // 先对数据进行排序
    const sortedData = [...data].sort((a, b) => a - b);

    // 计算最小值、Q1、中值、Q3、最大值
    const min = sortedData[0];
    const q1 = percentile_r2(sortedData, 0.25);
    const median = percentile_r2(sortedData, 0.5);
    const q3 = percentile_r2(sortedData, 0.75);
    const max = sortedData[sortedData.length - 1];

    return [ min, q1, median, q3, max ];
}

// 辅助函数，计算百分位数
function percentile_r2(arr, p) {
    if (arr.length === 0) return 0;
    const sorted = [...arr].sort((a, b) => a - b);
    const index = Math.floor(p * (sorted.length - 1));
    return sorted[index];
}

// 使用 ECharts 创建箱线图
function createBoxplot_r2(data) {
    let chartContainer = document.getElementById('right2');
    let myChart = echarts.init(chartContainer);

    let option = {
        title: {
            text: 'Health Distribution in Position',
            left: 'center',
            textStyle: {
                fontSize: 12
            },
            top: 5
        },
        tooltip: {
            trigger: 'item',
            axisPointer: {
                type: 'shadow'
            },
            top: 25
        },
        grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
        },
        xAxis: {
            type: 'category',
            data: data.categories,
            boundaryGap: false,
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
            min: 1000
        },
        series: [
            {
                type: 'boxplot',
                data: data.values,
                tooltip: {
                    formatter: function (param) {
                        return [
                            'Category: ' + param.name,
                            'Max: ' + param.data[5],
                            'Q3: ' + param.data[4],
                            'Median: ' + param.data[3],
                            'Q1: ' + param.data[2],
                            'Min: ' + param.data[1]
                        ].join('<br/>');
                    }
                }
            }
        ]
    };

    myChart.setOption(option);
}
