document.addEventListener('DOMContentLoaded', function() {
    // 현재 시간 표시 (정적 콘텐츠 영역)
    function updateCurrentTime() {
        const now = new Date();
        const options = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        };
        document.getElementById('current-time').textContent = now.toLocaleString('ko-KR', options);
    }

    // 초기 시간 설정 및 1초마다 업데이트
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);

    // PHP 서버 정보 불러오기 버튼 이벤트
    document.getElementById('load-php-btn').addEventListener('click', function() {
        const outputDiv = document.getElementById('php-output');
        outputDiv.innerHTML = '<p>서버 정보를 불러오는 중...</p>';

        fetch('server_info.php')
            .then(response => response.json())
            .then(data => {
                let html = '';
                html += `<div class="server-info"><span>서버 소프트웨어:</span> ${data.server_software}</div>`;
                html += `<div class="server-info"><span>PHP 버전:</span> ${data.php_version}</div>`;
                html += `<div class="server-info"><span>서버 시간:</span> ${data.server_time}</div>`;
                html += `<div class="server-info"><span>메모리 사용량:</span> ${data.memory_usage}</div>`;
                html += `<div class="server-info"><span>로드 시간:</span> ${data.load_time}ms</div>`;

                outputDiv.innerHTML = html;
            })
            .catch(error => {
                outputDiv.innerHTML = `<p>오류 발생: ${error.message}</p>`;
            });
    });
});