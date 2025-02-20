<?php
// 시작 시간 기록
$start_time = microtime(true);

// 메모리 사용량 시작 기록
$memory_start = memory_get_usage();

// 지연 시뮬레이션 (실제 API 호출이나 DB 쿼리 대체)
usleep(rand(100000, 300000));

// 서버 정보 수집
$server_info = [
    'server_software' => $_SERVER['SERVER_SOFTWARE'],
    'php_version' => phpversion(),
    'server_time' => date('Y년 m월 d일 H시 i분 s초'),
    'memory_usage' => round((memory_get_usage() - $memory_start) / 1024, 2) . ' KB',
    'load_time' => round((microtime(true) - $start_time) * 1000, 2)
];

// JSON 헤더 설정
header('Content-Type: application/json');
header('Cache-Control: no-cache, must-revalidate');

// 결과 출력
echo json_encode($server_info);
?>