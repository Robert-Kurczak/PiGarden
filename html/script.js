//--------------------------SEN0193 each values menu--------------------------
var menu_showed = false;
var pi_data_margin;

window.onload = function(){pi_data_margin = (document.getElementById("sensors_values").childElementCount / 2) * 3.5;}

function SensorsDropdown(){
    values = document.getElementById("sensors_values");
    arrow = document.getElementById("sensor_arrow");

    pi_data = document.getElementById("pi_data");

    if(!menu_showed){
        //handling css
        window.setTimeout(function(){values.style.marginLeft = "25%";}, 200);
        arrow.style.transform = "rotate(90deg)";
        pi_data.style.marginTop = pi_data_margin.toString() + "%";
        //---

        menu_showed = true;
    }
    else{
        //handling css
        values.style.marginLeft = "-85%";
        arrow.style.transform = "rotate(-90deg)";
        window.setTimeout(function(){pi_data.style.marginTop = "3.5%";}, 200);
        //---

        menu_showed = false;
    }
}
//----------------------------------------------------------------------------

//--------asynchronous executing commands from Bash_Commands.php file---------
function SendCMD(cmd){
    var measure_xhttp = new XMLHttpRequest();
    measure_xhttp.open("GET", "Bash_Commands.php?cmd=" + cmd, true);
    measure_xhttp.send();
}
//----------------------------------------------------------------------------

//-------------------------Pump and Lighting switches-------------------------
var pump_switch_active = false;
var LED_switch_active = false;

function SwitchSliders(ID, PassCMD=true){
    var border = document.getElementById(ID);
    var slider = border.childNodes[1];

    //return to default states function
    function cleanup(){
        border.style.border = "2px solid white";
        slider.style.left = "3px";
        slider.style.boxShadow = "0 0 0 0";

        if(ID == "pump_switch"){
            pump_switch_active = false;
        }
        else if(ID == "LED_switch"){
            LED_switch_active = false;
        }
    }
    //---

    if(ID == "pump_switch"){
        if(!pump_switch_active){
            //handling CSS
            border.style.border = "2px solid #32348B";
            slider.style.left = "37px";
            slider.style.boxShadow = "0px 0px 10px 4px rgba(240, 52, 88, 0.6)";
            //---
            pump_switch_active = true;
               
            if(PassCMD){SendCMD("PumpOn");}
        }
        else{
            if(PassCMD){SendCMD("PumpOff");}
            cleanup()
        }
    }

    else if(ID == "LED_switch"){
        if(!LED_switch_active){
            //handling CSS
            border.style.border = "2px solid #BC2387";
            slider.style.left = "37px";
            slider.style.boxShadow = "0px 0px 10px 4px rgba(7, 195, 241, 0.6)";
            //---
            LED_switch_active = true;

            if(PassCMD){SendCMD("LightingOn");}
        }
        else{
            if(PassCMD){SendCMD("LightingOff");}
            cleanup()
        }
    }
}
//-----------------------------------------------------------------------------

//------------------auto switching buttons if hardware is active---------------
fetch("Do_Not_Touch/Active_hardware.json", {cache: "no-store"})
    .then((response) => {
        return response.json()
    })

    .then((hardware_states) => {
        if(hardware_states["Pump"]){SwitchSliders("pump_switch", PassCMD=false);}
        if(hardware_states["Lighting"]){SwitchSliders("LED_switch", PassCMD=false);}
    })
//-----------------------------------------------------------------------------

//-----------------------------Take measure button-----------------------------
var measuring = false;

function TakeMeasure(){
    //prevent from multiple function calls
    if(measuring){
        return;
    }
    measuring = true;
    //---

    button = document.getElementById("measure_button");
    label = document.getElementById("measure_label");

    //handling CSS
    button.style.boxShadow = "0px 0px 10px 2px #F03458, 0px 0px 10px 4px #BC2387 inset";
    button.style.transitionDuration = "0.8s";
    button.style.width = "130px";
    label.style.marginLeft = "5%";

    button.style.fontFamily = "PoppinsLight";
    button.innerHTML = "Ładowanie...";
    //---

    //asynchronous sleep function
    async function AsyncSleep(time){
        await new Promise(resolve => setTimeout(resolve, time));
        StatusCheck();
    }
    //---

    //Scanning json file every second, waiting for correct finish status of measuring script
    async function StatusCheck(){
        fetch("Do_Not_Touch/Active_software.json", {cache: "no-store"})
            .then((response) => {
                return response.json();
            })

            .then((software_states) => {
                if(software_states["Measure"] == "need watering"){
                    SendCMD("TakeMeasure"); //Clear Active_software

                    //return to default css
                    button.style.width = "35px";
                    label.style.marginLeft = "24%";
                    //
                    window.alert("Ogród wymaga podlania.");
                    
                    SendCMD("Watering");    //Start pumping

                    window.setTimeout(function(){location.reload()}, 500)

                }
                else if(software_states["Measure"] == "done"){
                    SendCMD("TakeMeasure"); //Clear Active_software

                    //return to default css
                    button.style.width = "35px";
                    label.style.marginLeft = "24%";
                    //
                    
                    window.setTimeout(function(){location.reload()}, 1000)
                }
                else{
                    console.log("asdas");
                    AsyncSleep(1000);
                }
            })
    }
    //---

    SendCMD("TakeMeasure");
    StatusCheck();
}
