<?php
    switch($_GET["cmd"]){
        case "PumpOn":
            shell_exec("cd /home/pi && /usr/bin/python3 -c 'from Pump import water_pump; water_pump.on()'");
	        break;

        case "PumpOff":
            shell_exec("cd /home/pi && /usr/bin/python3 -c 'from Pump import water_pump; water_pump.off()'");
            break;

        case "LightingOn":
            shell_exec("cd /home/pi && /usr/bin/python3 -c 'from Lighting import grow_light; grow_light.on()'");
            break;

        case "LightingOff":
            shell_exec("cd /home/pi && /usr/bin/python3 -c 'from Lighting import grow_light; grow_light.off()'");
            break;

        case "TakeMeasure":
            //returning state from json file
            function ReadState(){
                $active_software = json_decode(file_get_contents("Do_Not_Touch/Active_software.json"), true);
                return $active_software["Measure"];
            }
            //---

            //changing state in json file
            function ChangeState($state){
                $active_software = json_decode(file_get_contents("Do_Not_Touch/Active_software.json"), true);
                $active_software["Measure"] = $state;

                $json_file = fopen("Do_Not_Touch/Active_software.json", "w");
                fwrite($json_file, json_encode($active_software));
            }
            //---

            if(ReadState() != false){
                ChangeState(false);
                break; //idk why it doesn't stop this case block
            }
            else{
                shell_exec("cd /home/pi && /usr/bin/python3 -c 'from Measure import take_measure; take_measure(auto_wtr=False)'");
            }

            break;

        case "Watering":
            shell_exec("cd /home/pi && /usr/bin/python3 -c 'from Pump import water_pump; water_pump.pump(40)'");
        }
?>