document.addEventListener('DOMContentLoaded', function () {
    // 使用 fetch 从后端获取数据
    // 替换 '/your-backend-endpoint' 为实际的后端端点
    fetch('/min_max_speed_each_position')
        .then(response => response.json())
        .then(data => {
            // 处理 JSON 数据为 ECharts 所需格式
            let processedData = processData_b1(data);
            // 使用 ECharts 创建雷达图
            createRadarChart_b1(processedData);
        })
        .catch(error => console.error('Error fetching data:', error));
});

// 处理 JSON 数据为 ECharts 所需格式
function processData_b1(data) {
    let processedData = {
        departments: [],
        minValues: [],
        maxValues: []
    };

    for (let i = 0; i < data.length; i++) {
        processedData.departments.push(data[i].Position);
        processedData.minValues.push(data[i].Slowest);
        processedData.maxValues.push(data[i].Fastest);
    }

    return processedData;
}

// 使用 ECharts 创建雷达图
function createRadarChart_b1(data) {
    let chartContainer = document.getElementById('bottom2');
    let myChart = echarts.init(chartContainer);

    let option = {
        title: {
            text: 'Salary Range in Departments',
            left: 'center',
            textStyle: {
                fontSize: 12 // 设置字体大小
            },
            top: 5
        },
        legend: {
            data: ['Minimum Speed', 'Maximum Speed'],
            top: 25
        },
        radar: {
            indicator: data.departments.map(function (department) {
                return { name: department, max: 600 };
            }),
            center: ['50%', '60%'],
        },
        series: [
            {
                name: 'Speed Range',
                type: 'radar',
                data: [
                    {
                        value: data.minValues,
                        name: 'Minimum Speed'
                    },
                    {
                        value: data.maxValues,
                        name: 'Maximum Speed'
                    }
                ],
                label: {
                    show: false,
                    formatter: function (params) {
                        return params.value.toFixed(2);
                    }
                }
            }
        ],
        tooltip: {
            show: true,
            formatter: function (params) {
                let name = data.departments[params.dataIndex];
                let dataIndex = params.dataIndex;
                let minValue = data.minValues[dataIndex].toFixed(2);
                let maxValue = data.maxValues[dataIndex].toFixed(2);
                return name + ' : ' + minValue + ' M - ' + maxValue + ' M';
            }
        },
        axisPointer: {
            label: {
                show: true,
                formatter: function (params) {
                    let dataIndex = params.dataIndex;
                    let value = params.value.toFixed(2);
                    if (params.axisIndex === 0) {
                        value = data.minValues[dataIndex].toFixed(2);
                    } else if (params.axisIndex === 1) {
                        value = data.maxValues[dataIndex].toFixed(2);
                    }
                    return value;
                }
            },
            type: 'line',
            triggerAction: 'axis'
        },
        radarText: {
            show: true,
            formatter: function (params) {
                let dataIndex = params.dataIndex;
                let minValue = data.minValues[dataIndex].toFixed(2);
                let maxValue = data.maxValues[dataIndex].toFixed(2);
                return params.name + ' : ' + minValue + ' M - ' + maxValue + ' M';
            },
            distance: 15
        }
    };


    myChart.setOption(option);
}