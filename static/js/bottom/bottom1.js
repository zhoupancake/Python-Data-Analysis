document.addEventListener('DOMContentLoaded', function () {
    // 使用 fetch 从后端获取数据
    // 替换 '/your-backend-endpoint' 为实际的后端端点
    fetch('/type_count_each_position')
        .then(response => response.json())
        .then(data => {
            // 处理 JSON 数据为 ECharts 所需格式
            let processedData = processData_b2(data);

            // 使用 ECharts 创建柱状图
            createBarChart_b2(processedData);
        })
        .catch(error => console.error('Error fetching data:', error));
});

// 处理 JSON 数据为 ECharts 所需格式
function processData_b2(data) {
    let processedData = {
        departments: [],
        femaleCount: [],
        maleCount: []
    };

    for (let i = 0; i < data.length; i++) {
        processedData.departments.push(data[i].Position);
        processedData.femaleCount.push(data[i].Magic);
        processedData.maleCount.push(data[i].Physical);
    }

    return processedData;
}

// 使用 ECharts 创建柱状图
function createBarChart_b2(data) {
    let chartContainer = document.getElementById('bottom1');
    let myChart = echarts.init(chartContainer);

   let option = {
        title: {
            text: 'Type Distribution in Positions',
            left: 'center',
            textStyle: {
                fontSize: 12 // 设置字体大小
            },
            top: 5
        },
        legend: {
            data: ['Magic', 'Physical'],
            top: 25
        },
        xAxis: {
            type: 'category',
            data: data.departments,
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
                name: 'Magic',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    formatter: function (params) {
                        return params.value;
                    }
                },
                emphasis: {
                    focus: 'series'
                },
                data: data.femaleCount
            },
            {
                name: 'Physical',
                type: 'bar',
                stack: 'total',
                label: {
                    show: true,
                    formatter: function (params) {
                        return params.value;
                    }
                },
                emphasis: {
                    focus: 'series'
                },
                data: data.maleCount
            }
        ],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
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