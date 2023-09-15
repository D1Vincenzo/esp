html = ...
'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 Light Control</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: rgba(0, 0, 0, 0.2); /* 默认为较亮的背景 */
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
            transition: background-color 0.5s; /* 添加过渡效果 */
        }

        .light-off {
            background-color: rgba(0, 0, 0, 0.7); /* 当灯泡熄灭时，背景变为较暗 */
        }

        .bulb {
            fill: yellow;
            transition: fill 0.5s;
            cursor: pointer;
        }

        .bulb-off {
            fill: #ccc;
        }

        /* 设置按钮样式 */
        .settings-btn {
            position: absolute;
            bottom: 10px;
            left: 10px;
            background-color: #333;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .settings-btn:hover {
            background-color: #555;
        }

        /* 模态窗口样式 */
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            visibility: hidden;
            opacity: 0;
            transition: visibility 0s, opacity 0.3s;
        }

        .modal-content {
            position: relative;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            width: 300px;
            max-width: 80%;
        }

        .modal.active {
            visibility: visible;
            opacity: 1;
        }

        .close-btn {
            position: absolute;
            right: 10px;
            top: 10px;
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
        }

        .countdown {
        transition: x 1s, fill-opacity 1s;
    }
</style>
    </style>
</head>
<body class="light-on" onmousedown="startSwipe(event)" onmousemove="swipe(event)" onmouseup="endSwipe()">
    <!-- 灯泡部分 -->
    <svg width="100vw" height="100vh" viewBox="0 0 100 150">
        <circle class="bulb" cx="50" cy="50" r="40" onclick="toggleLight()"></circle>
        <text id="countdown" x="50" y="55" font-size="10" text-anchor="middle" fill="#333">1</text>
        
        <!-- 左侧三角形移到灯泡的左侧 -->
        <polygon id="decreaseButton" points="5,50 15,45 15,55" fill="#333" onclick="decreaseCountdown()"></polygon>
        
        <!-- 右侧三角形移到灯泡的右侧 -->
        <polygon id="increaseButton" points="95,50 85,45 85,55" fill="#333" onclick="increaseCountdown()"></polygon>
        
        <rect x="40" y="90" width="20" height="40" fill="#666"></rect>
    </svg>



    <!-- 设置按钮 -->
    <button class="settings-btn" onclick="openModal()">Settings</button>

    <!-- 模态窗口 -->
    <div class="modal" id="settingsModal">
        <div class="modal-content">
            <button class="close-btn" onclick="closeModal()">&times;</button>
            <h3>Settings</h3>
            <!-- 这里可以添加设置内容 -->

            <!-- 1. 亮度调节 -->
            <div>
                <label for="brightness">Brightness:</label>
                <input type="range" id="brightness" min="0" max="100" value="100">
            </div>

            <!-- 2. 颜色选择 -->
            <div>
                <label for="colorPicker">Color:</label>
                <input type="color" id="colorPicker" value="#ffff00">
            </div>

            <!-- 3. 定时开关 -->
            <div>
                <label for="defaultCountdown">Default Countdown:</label>
                <input type="number" id="defaultCountdown" min="1" value="1">
            </div>
            
            <!-- 4. 灯泡模式 -->
            <div>
                <label for="mode">Mode:</label>
                <select id="mode">
                <option value="normal">Normal</option>
                <option value="blink">Blink</option>
                <option value="fade">Fade</option>
                </select>
            </div>
            
            <!-- 5. 恢复默认设置 -->
            <div>
                <button onclick="resetSettings()">Restore Defaults</button>
            </div>
            
            <!-- 6. 反馈与支持 -->
            <div>
                <h4>Feedback & Support:</h4>
                <p>If you encounter any issues or have suggestions, please <a href="">contact us</a>.</p>
            </div>


        </div>
    </div>

    <script>
        let isLightOn = true;
        let countdownInterval;
        const countdownElement = document.getElementById('countdown');


        function toggleLight() {
            const bulb = document.querySelector('.bulb');
            const body = document.querySelector('body');
            const defaultCountdownValue = parseInt(document.getElementById('defaultCountdown').value) || 1;

            clearInterval(countdownInterval); // 清除已存在的定时器

            if (isLightOn) {
                // 从当前显示的值开始倒计时
                let timerValue = parseInt(countdownElement.textContent) || defaultCountdownValue;
                countdownElement.setAttribute('visibility', 'visible'); // 确保倒计时始终可见
                if (timerValue >= 1) {
                    countdownInterval = setInterval(() => {
                        timerValue--;
                        countdownElement.textContent = timerValue;
                        if (timerValue <= 0) {
                            clearInterval(countdownInterval);
                            bulb.classList.add('bulb-off');
                            body.classList.remove('light-on');
                            body.classList.add('light-off');
                            countdownElement.setAttribute('visibility', 'hidden');
                            sendCommand('lightoff');
                            isLightOn = false;
                        }
                    }, 1000);
                } else {
                    bulb.classList.add('bulb-off');
                    body.classList.remove('light-on');
                    body.classList.add('light-off');
                    countdownElement.setAttribute('visibility', 'hidden');
                    sendCommand('lightoff');
                    isLightOn = false;
                }
            } else {
                bulb.classList.remove('bulb-off');
                body.classList.add('light-on');
                body.classList.remove('light-off');
                countdownElement.textContent = defaultCountdownValue.toString();
                countdownElement.setAttribute('visibility', 'visible');
                sendCommand('lighton');
                isLightOn = true;
            }
        }





    
        // 函数：向后端（例如ESP32）发送命令
        function sendCommand(cmd) {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/' + cmd, true);
            xhr.send();
        }
    
        // 函数：打开设置窗口
        function openModal() {
            document.getElementById('settingsModal').classList.add('active');
        }
    
        // 函数：关闭设置窗口
        function closeModal() {
            document.getElementById('settingsModal').classList.remove('active');
        }
    
        // 函数：将设置重置为默认值
        function resetSettings() {
            document.getElementById('brightness').value = 100;
            document.getElementById('colorPicker').value = "#ffff00";
            document.getElementById('timer').value = "";
            document.getElementById('mode').value = "normal";
        }

        function decreaseCountdown() {
            let currentValue = parseInt(countdownElement.textContent) || 0;
            if (currentValue > 1) {
                countdownElement.textContent = currentValue - 1;
            }
        }

        function increaseCountdown() {
            let currentValue = parseInt(countdownElement.textContent) || 0;
            countdownElement.textContent = currentValue + 1;
        }
        
        let isSwiping = false;
        let startX = 0;

        function startSwipe(e) {
            isSwiping = true;
            startX = e.clientX;
        }

        function swipe(e) {
            if (!isSwiping) return;

            const deltaX = e.clientX - startX;  // 计算横向滑动的距离

            if (deltaX > 50) {  
                decreaseCountdown();  // 向右滑动时减少计时器
                startX = e.clientX;
            } else if (deltaX < -50) {  
                increaseCountdown();  // 向左滑动时增加计时器
                startX = e.clientX;
            }

        }

        function endSwipe() {
            isSwiping = false;
        }

    </script>
    
    
    
</body>
</html>
'''