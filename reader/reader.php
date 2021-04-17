<?php

require_once "vendor/autoload.php";

use Graby\Graby;

$defaultUseragent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.92 Safari/535.2';

$customUseragent = "HNClient (in development)";

$userAgent = $defaultUseragent . " " . $customUseragent;

$url = file_get_contents("php://stdin");


$graby = new Graby([
    "http_client" => [
        'ua_browser' => $userAgent,
    ]
]);

$result = $graby->fetchContent($url);
echo json_encode($result);
