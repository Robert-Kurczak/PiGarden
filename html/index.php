<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="icon" type="image/svg" href="CSS/favicon.svg"/>
    <title>PiGarden</title>

    <link rel="stylesheet" href="CSS/style.css">
    <script src="script.js"></script>

</head>
<body>

    <?php
        $connection = mysqli_connect("localhost", "remoteAccess", "PiGardenRemote", "PiGarden");

        $air_temperature = mysqli_fetch_row(mysqli_query($connection, "SELECT `Value` FROM `Air_Temperature` ORDER BY `Date` DESC LIMIT 1"))[0]."°C";
        if($air_temperature == "°C"){$air_temperature = "Brak danych";} //handling nulls

        $air_humidity = mysqli_fetch_row(mysqli_query($connection, "SELECT `Value` FROM `Air_Humidity` ORDER BY `Date` DESC LIMIT 1"))[0]."%";
        if($air_humidity == "%"){$air_humidity = "Brak danych";}    //handling nulls

        $soil_moisture = [];    //[[value, channel]]
        $soil_moisture_sum = 0; //need for avg value

        //date of the latest SEN0193 reads
        $youngest_date = new DateTime(mysqli_fetch_row(mysqli_query($connection, "SELECT `Date` FROM `Soil_Moisture` ORDER BY `Date` DESC LIMIT 1"))[0]);

        for($i = 0; $i < 8; $i++){
            //date of the current checking reads
            $date = new DateTime(mysqli_fetch_row(mysqli_query($connection, "SELECT `Date` FROM `Soil_Moisture` WHERE `Channel` = $i ORDER BY `Date` DESC LIMIT 1"))[0]);
            
            //difference between $youngest_date and $date in minutes
            //if less than 5 minutes
            if(($youngest_date->getTimestamp() - $date->getTimestamp()) / 60 <= 5){
                    $sensor_value = mysqli_fetch_row(mysqli_query($connection, "SELECT `Value` FROM `Soil_Moisture` WHERE `Channel` = $i ORDER BY `Date` DESC LIMIT 1"))[0];

                    //handling nulls
                    if($sensor_value != NULL){
                        $soil_moisture_sum += $sensor_value;
                        array_push($soil_moisture, [$sensor_value, $i]);
                    }
            }
        }

        if(count($soil_moisture)){
            $soil_moisture_avg = round($soil_moisture_sum / count($soil_moisture), 2)."%";
        }
        else{
            $soil_moisture_avg = "Brak danych";
        }

    ?>

    <div id="upper_body">
        <div id="info">

            <div id="temperature">
                <p>Temperatura otoczenia: <span class="values"><?php echo("$air_temperature"); ?></span></p>
                <div class="info_stripes"></div>
            </div>

            <div id="humidity">
                <p>Wilgotność powietrza: <span class="values"><?php echo("$air_humidity"); ?></span></p>
                <div class="info_stripes"></div>
            </div>

            <div id="moisture">
                <?php
                    if(count($soil_moisture)){
                        echo("
                            <!--Sensors values dropdown arrow svg-->
                            <svg id =\"sensor_arrow\" onclick=\"SensorsDropdown()\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" fill=\"white\">
                                <path d=\"M10 17l5-5-5-5v10z\"/>
                                <path d=\"M0 24V0h24v24H0z\" fill=\"none\"/>
                            </svg>
                            <!--------------------------------->
                        ");
                    }
                ?>

                <p>Wilgotność gleby: <span class="values"><?php echo("$soil_moisture_avg"); ?></span></p>
                <div class="info_stripes"></div>

                <div id="sensors_values">
                    <?php

                        for($i = 0; $i < count($soil_moisture); $i++){
                                $channel = $soil_moisture[$i][1];
                                $value = $soil_moisture[$i][0];

                            echo("
                                <p>Sensor $channel: <span class=\"values\">$value%</span></p>
                                <div class=\"info_stripes\"></div>
                            ");
                        }

                    ?>

                </div>

            </div>

        </div>

        <div id="switches">

            <div class="switch_holder">
                <div class="switch" id="pump_switch" onclick="SwitchSliders('pump_switch')">
                    <span class="slider"></span>
                </div>
                <p class="switch_label">Włącznik pompy</p>
            </div>

            <div class="switch_holder">
                <div class="switch" id="LED_switch" onclick="SwitchSliders('LED_switch')">
                    <span class="slider"></span>
                </div>
                <p class="switch_label">Włącznik LED</p>
            </div>

            <div class="switch_holder">
                <button id="measure_button" onclick="TakeMeasure()"></button>
                <p id="measure_label">Zrób pomiar</p>            
            </div>

        </div>
    </div>

    <div id="pi_data">
        <p id="pi_data_label">Raspberry Pi <img id="pi_logo" src="CSS/pi_logo.svg"></p>

        <p class="pi_data_values">Temperatura procesora: 
            <?php 
                echo(mysqli_fetch_row(mysqli_query($connection, "SELECT `CPU_temp` FROM `Pi_Data` ORDER BY `ID` DESC LIMIT 1;"))[0]."°C");
            ?>
        </p>

        <p class="pi_data_values">Czas pracy systemu: 
            <?php
                echo(gmdate("H:i:s", mysqli_fetch_row(mysqli_query($connection, "SELECT `Sys_uptime` FROM `Pi_Data` ORDER BY `ID` DESC LIMIT 1;"))[0]));
            ?>
        </p>

        <p class="pi_data_values">Wersja systemu: 
            <?php
                echo(mysqli_fetch_row(mysqli_query($connection, "SELECT `Sys_version` FROM `Pi_Data` ORDER BY `ID` DESC LIMIT 1;"))[0]);
            ?>
        </p>
    
    </div>

    <div id="charts">

        <div class="chart">
            <canvas id="humidity_canvas" width="400" height="400"></canvas>
        </div>

        <div class="chart">
            <canvas id="temperature_canvas" width="400" height="400"></canvas>
        </div>

    </div>
    
    <?php

        $chart_temperature_values = array();
        $chart_temperature_dates = array();

        $chart_humidity_values = array();
        $chart_humidity_dates = array();

        for($i = 6; $i >= 0; $i--){
            //closest values to 12:00
            $temperature_query = mysqli_fetch_row(mysqli_query($connection, "SELECT `Value`, `Date` FROM `Air_Temperature` WHERE DATE(`Date`) = CURDATE() - INTERVAL $i DAY ORDER BY ABS(TIME(`DATE`) - INTERVAL 12 HOUR) LIMIT 1"));
            $humidity_query = mysqli_fetch_row(mysqli_query($connection, "SELECT `Value`, `Date` FROM `Air_Humidity` WHERE DATE(`Date`) = CURDATE() - INTERVAL $i DAY ORDER BY ABS(TIME(`DATE`) - INTERVAL 12 HOUR) LIMIT 1;"));

            //handling nulls
            if(!$temperature_query){
                array_push($chart_temperature_values, 0);
                array_push($chart_temperature_dates, "Brak danych");
            }
            else{
                array_push($chart_temperature_values, (int)$temperature_query[0]);
                array_push($chart_temperature_dates, array(substr($temperature_query[1], 0, 10), substr($temperature_query[1], 11)));
            }

            if(!$humidity_query){
                array_push($chart_humidity_values, 0);
                array_push($chart_humidity_dates, "Brak danych");
            }
            else{
                array_push($chart_humidity_values, (int)$humidity_query[0]);
                array_push($chart_humidity_dates, array(substr($humidity_query[1], 0, 10), substr($humidity_query[1], 11)));
            }
        }
        
        mysqli_close($connection);

        //php array to js array
        $chart_temperature_values = json_encode($chart_temperature_values);
        $chart_temperature_dates = json_encode($chart_temperature_dates);

        $chart_humidity_values = json_encode($chart_humidity_values);
        $chart_humidity_dates = json_encode($chart_humidity_dates);

        //php to js
        echo("  
                <script>  
                        var chart_temperature_values = $chart_temperature_values;
                        var chart_temperature_dates = $chart_temperature_dates;

                        var chart_humidity_values = $chart_humidity_values;
                        var chart_humidity_dates = $chart_humidity_dates;

                </script>"
            );
    ?>

    <script src="ChartJS/Chart.min.js"></script>
    <script src="ChartJS/ChartsConfig.js"></script>

</body>
</html>
