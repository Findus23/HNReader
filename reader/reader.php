<?php

require_once "vendor/autoload.php";

use Graby\Graby;

$url = file_get_contents("php://stdin");


$graby = new Graby();

$result = $graby->fetchContent($url);
echo json_encode($result);
