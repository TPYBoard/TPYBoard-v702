<?php

     $backstr = "error";
     $getStr = $_GET["t"];
     if($getStr!=""){
       $backstr = "{\"status\":\"0\",\"method\":\"GET\",\"data\":\"".$getStr."\"}";
     }else{
      $postStr = file_get_contents("php://input");
      if($postStr!=""){
        $backstr = "{\"status\":\"0\",\"method\":\"POST\",\"data\":\"".$postStr."\"}";
      }
    }
    echo $backstr;
    
?>