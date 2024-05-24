// 显示数据的函数
    function showData(data) {
        let dataContainer = document.getElementById('data-container');
        dataContainer.innerHTML = data;
        dataContainer.style.display = 'block';
    }

    // 隐藏数据的函数
    function hideData() {
        let dataContainer = document.getElementById('data-container');
        dataContainer.style.display = 'none';
    }

    // 获取图标元素
    let icons = document.querySelectorAll('.icon');

    // 添加鼠标悬停事件监听器
    icons.forEach(function (icon) {
        icon.addEventListener('mouseover', function () {
            // 获取数据
            let data = icon.innerText;
            // 显示数据
            showData('Data for Icon ' + data);
        });

        icon.addEventListener('mouseout', function () {
            // 鼠标移开时隐藏数据
            hideData();
        });
    });