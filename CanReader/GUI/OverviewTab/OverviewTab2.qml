import QtQuick 2.12
import QtQuick.Extras 1.4
import QtQuick.Controls 2.3
import QtQuick.Controls.Styles 1.4

Item {
    id: element
    width: 1080
    height: 720

    Connections {
        target: slider
        onValueChanged: {
            rpmGauge.value = slider.value
            cltGauge.value = slider.value
            oilTmpGauge.value = slider.value
            oilPressureGauge.value = slider.value
            fuelPressureGauge.value = slider.value
            fl_dumper.value = slider.value + 5
            fr_dumper.value = slider.value + 5
            rl_dumper.value = slider.value - 5
            rr_dumper.value = slider.value - 5
            throttleGauge.value = slider.value
            brakeGauge.value = slider.value
            batteryValue.text = slider.value
        }
    }

    Connections {
        target: centerButton
        onClicked: {
            flDumperGauge.minimumValue = parseInt(flDumperGauge.value - 25/2)
            flDumperGauge.maximumValue = parseInt(flDumperGauge.value + 25/2)
            frDumperGauge.minimumValue = parseInt(frDumperGauge.value - 25/2)
            frDumperGauge.maximumValue = parseInt(frDumperGauge.value + 25/2)
            rlDumperGauge.minimumValue = parseInt(rlDumperGauge.value - 25/2)
            rlDumperGauge.maximumValue = parseInt(rlDumperGauge.value + 25/2)
            rrDumperGauge.minimumValue = parseInt(rrDumperGauge.value - 25/2)
            rrDumperGauge.maximumValue = parseInt(rrDumperGauge.value + 25/2)
            coolantFanState.active = true;
            fuelPumpState.active = true;
        }
    }

    Connections {
        target: batteryValue
        onTextChanged:{
            if(parseInt(batteryValue.text) < 11 && batteryImg.source != "battery_low.png"){
                batteryImg.source = "battery_low.png"
            }else
            {
                batteryImg.source = "battery_normal.png"
            }
        }
    }

    Connections{
        target: cltGauge
        onValueChanged:{
            if(cltGauge.value >= 125 || parseInt(CLT_sensor.value) === 1 ){
                waterTempStatus.source = "water_temp_error.png"
            }
            else if((cltGauge.value > 115) && (cltGauge.value < 125)){
                waterTempStatus.source = "water_temp_warning.png"
            }else{
                waterTempStatus.source = "water_temp_normal.png"
            }
        }
    }

    Connections{
        target: oilPressureGauge
        onValueChanged:{
            if(oilPressureGauge.value > 8){
                oilPressureStatus.source = "oil_pres_error.png"
            }
            else if(oilPressureGauge.value < 1){
                oilPressureStatus.source = "oil_pres_warning.png"
            }else{
                oilPressureStatus.source = "oil_pres_normal.png"
            }
        }
    }

    Connections{
        target: fuelPressureGauge
        onValueChanged:{
            if(fuelPressureGauge.value > 4 || parseInt(WBO_sensor.value) === 1
                    || parseInt(FP_sensor.value) === 1 || parseInt(knock_detect.value) === 1){
                engineStatus.source = "engine_error.png"
            }
            else if(fuelPressureGauge.value < 1){
                engineStatus.source = "engine_warning.png"
            }else{
                engineStatus.source = "engine_normal.png"
            }
        }
    }

    Connections {
        target: gear
        onValueChanged:{
            if(parseInt(gear.value) === 0){
                gearValue.text = "N"
            }else
            {
                gearValue.text = gear.value
            }
        }
    }

    Connections {
        target: FPS
        onValueChanged:{
            if(parseInt(FPS.value) === 1){
                fuelPumpState.active = true;
            }else{
                fuelPumpState.active = false;
            }
        }
    }

    Connections {
        target: CFS
        onValueChanged:{
            if(parseInt(CFS.value) === 1){
                coolantFanState.active = true;
            }else{
                coolantFanState.active = false;
            }
        }
    }

    Rectangle {
        id: rectangle
        color: "#4f4e4e"
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0


        Item {
            id: secondaryOverview
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.top: mainOverview.bottom
            anchors.topMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0

            Item {
                id: suspension
                x: 843
                width: 237
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.bottomMargin: 0
                anchors.bottom: parent.bottom
                anchors.horizontalCenterOffset: secondaryOverview.width > 1300 ? (secondaryOverview.width/3 - width/2) : (secondaryOverview.width/3)
                anchors.horizontalCenter: parent.horizontalCenter
                Gauge {
                    id: flDumperGauge
                    width: 33
                    anchors.right: parent.horizontalCenter
                    anchors.rightMargin: 60
                    anchors.bottom: parent.verticalCenter
                    anchors.bottomMargin: 10
                    anchors.topMargin: 0
                    anchors.top: suspension_text.bottom
                    tickmarkStepSize: 0
                    value: fl_dumper.value
                    minimumValue: 25
                    maximumValue: 50

                    Behavior on value {
                        NumberAnimation {
                            duration: 100
                        }
                    }

                    style: GaugeStyle {
                        valueBar: Rectangle {
                            color: Qt.rgba(1 +flDumperGauge.value / flDumperGauge.maximumValue, 1 - flDumperGauge.value / flDumperGauge.maximumValue, 0, 1)
                            implicitWidth: 16
                        }
                    }

                    Label {
                        id: fllabel
                        height: 16
                        color: "#bdbebf"
                        text: qsTr("FL")
                        anchors.topMargin: -4
                        verticalAlignment: Text.AlignVCenter
                        anchors.leftMargin: 8
                        anchors.right: parent.right
                        anchors.top: parent.bottom
                        anchors.left: parent.left
                        anchors.rightMargin: 0
                        horizontalAlignment: Text.AlignHCenter
                    }

                    Label {
                        id: flValue
                        x: -6
                        y: 36
                        color: "#ffffff"
                        text: parseFloat(fl_dumper.value).toFixed(2)
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        anchors.rightMargin: 0
                        rotation: -90
                    }
                }

                Gauge {
                    id: frDumperGauge
                    width: 33
                    anchors.left: parent.horizontalCenter
                    anchors.leftMargin: 50
                    anchors.bottom: parent.verticalCenter
                    anchors.bottomMargin: 10
                    anchors.topMargin: 0
                    anchors.top: suspension_text.bottom
                    tickmarkStepSize: 0
                    value: fr_dumper.value
                    minimumValue: 25
                    maximumValue: 50

                    Behavior on value {
                        NumberAnimation {
                            duration: 100
                        }
                    }

                    style: GaugeStyle {
                        valueBar: Rectangle {
                            color: Qt.rgba(1 +frDumperGauge.value / frDumperGauge.maximumValue, 1 - frDumperGauge.value / frDumperGauge.maximumValue, 0, 1)
                            implicitWidth: 16
                        }
                    }

                    Label {
                        id: frlabel
                        height: 16
                        color: "#bdbebf"
                        text: qsTr("FR")
                        anchors.topMargin: -4
                        anchors.leftMargin: 8
                        verticalAlignment: Text.AlignVCenter
                        anchors.top: parent.bottom
                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.rightMargin: 0
                        horizontalAlignment: Text.AlignHCenter
                    }

                    Label {
                        id: frValue
                        x: -6
                        y: 36
                        color: "#ffffff"
                        text: parseFloat(fr_dumper.value).toFixed(2)
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        anchors.rightMargin: 0
                        rotation: -90
                    }
                }

                Gauge {
                    id: rlDumperGauge
                    x: 11
                    width: 33
                    anchors.top: parent.verticalCenter
                    anchors.topMargin: 10
                    anchors.right: parent.horizontalCenter
                    anchors.rightMargin: 60
                    anchors.bottomMargin: 15
                    tickmarkStepSize: 0
                    anchors.bottom: parent.bottom
                    value: rl_dumper.value
                    minimumValue: 25
                    maximumValue: 50

                    Behavior on value {
                        NumberAnimation {
                            duration: 100
                        }
                    }

                    style: GaugeStyle {
                        valueBar: Rectangle {
                            color: Qt.rgba(1 +rlDumperGauge.value / rlDumperGauge.maximumValue, 1 - rlDumperGauge.value / rlDumperGauge.maximumValue, 0, 1)
                            implicitWidth: 16
                        }
                    }

                    Label {
                        id: rllabel
                        height: 16
                        color: "#bdbebf"
                        text: qsTr("RL")
                        anchors.right: parent.right
                        anchors.rightMargin: 0
                        anchors.left: parent.left
                        anchors.leftMargin: 8
                        anchors.topMargin: -4
                        verticalAlignment: Text.AlignVCenter
                        anchors.top: parent.bottom
                        horizontalAlignment: Text.AlignHCenter
                    }

                    Label {
                        id: rlValue
                        x: -6
                        y: 36
                        color: "#ffffff"
                        text: parseFloat(rl_dumper.value).toFixed(2)
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        anchors.rightMargin: 0
                        rotation: -90
                    }
                }

                Gauge {
                    id: rrDumperGauge
                    width: 33
                    anchors.left: parent.horizontalCenter
                    anchors.leftMargin: 50
                    anchors.top: parent.verticalCenter
                    anchors.topMargin: 10
                    anchors.bottomMargin: 15
                    tickmarkStepSize: 0
                    anchors.bottom: parent.bottom
                    value: rr_dumper.value
                    minimumValue: 25
                    maximumValue: 50

                    Behavior on value {
                        NumberAnimation {
                            duration: 100
                        }
                    }

                    style: GaugeStyle {
                        valueBar: Rectangle {
                            color: Qt.rgba(1 +rrDumperGauge.value / rrDumperGauge.maximumValue, 1 - rrDumperGauge.value / rrDumperGauge.maximumValue, 0, 1)
                            implicitWidth: 16
                        }
                    }

                    Label {
                        id: rrlabel
                        height: 16
                        color: "#bdbebf"
                        text: qsTr("RR")
                        anchors.topMargin: -4
                        verticalAlignment: Text.AlignVCenter
                        anchors.leftMargin: 8
                        anchors.right: parent.right
                        anchors.top: parent.bottom
                        anchors.left: parent.left
                        anchors.rightMargin: 0
                        horizontalAlignment: Text.AlignHCenter
                    }

                    Label {
                        id: rrValue
                        x: -6
                        y: 36
                        color: "#ffffff"
                        text: parseFloat(rr_dumper.value).toFixed(2)
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        anchors.rightMargin: 0
                        rotation: -90
                    }
                }

                Text {
                    id: suspension_text
                    x: 34
                    color: "#bdbebf"
                    text: qsTr("SUSPENSION")
                    anchors.horizontalCenterOffset: 0
                    anchors.top: parent.top
                    anchors.topMargin: 8
                    anchors.horizontalCenter: parent.horizontalCenter
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: 15
                }

                Button {
                    id: centerButton
                    x: 66
                    width: 58
                    height: 15
                    anchors.horizontalCenterOffset: 0
                    anchors.top: image.verticalCenter
                    anchors.topMargin: 83
                    anchors.horizontalCenter: parent.horizontalCenter

                    contentItem: Text {
                        text: qsTr("Center")
                        color: "#ffffff"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }
                    background: Rectangle {
                        implicitWidth: parent.width
                        implicitHeight: parent.height
                        border.width: 1
                        border.color: "#051a39"
                        radius: 4
                        gradient: Gradient {
                            GradientStop { position: 0.6 ; color: "#545454"}
                            GradientStop { position: 1.0 ; color: "#3B3B3B"}
                        }
                    }

                }

                Image {
                    id: image
                    x: -627
                    y: -66
                    width: 180
                    height: 120
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    rotation: -90
                    fillMode: Image.PreserveAspectFit
                    source: "formule.png"
                    anchors.verticalCenterOffset: 10
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }

            Item {
                id: stats
                x: 220
                width: 306
                height: 160
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.horizontalCenter: parent.horizontalCenter

                Text {
                    id: statsText
                    x: 57
                    color: "#bdbebf"
                    text: qsTr("STATS")
                    fontSizeMode: Text.Fit
                    anchors.top: parent.top
                    anchors.topMargin: 8
                    anchors.horizontalCenter: parent.horizontalCenter
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: 15
                }

                Image {
                    id: batteryImg
                    x: 135
                    y: 34
                    width: 36
                    height: 32
                    anchors.verticalCenterOffset: -40
                    visible: true
                    anchors.horizontalCenterOffset: 0
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    source: "battery_normal.png"
                    fillMode: Image.PreserveAspectFit

                    Label {
                        id: batteryValue
                        x: 3
                        y: 28
                        color: "#bdbebf"
                        text: "#parseFloat(battery.value).toFixed(2)#"
                        anchors.verticalCenterOffset: 30
                        anchors.horizontalCenterOffset: -5
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignRight

                        Label {
                            id: batteryUnitV
                            x: 39
                            y: 4
                            color: "#bdbebf"
                            text: qsTr("V")
                            anchors.horizontalCenterOffset: 25
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.verticalCenter: parent.verticalCenter
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                        }
                    }
                }

                Image {
                    id: engineStatus
                    x: 34
                    y: 99
                    width: 48
                    height: 50
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenterOffset: -80
                    anchors.horizontalCenter: parent.horizontalCenter
                    source: "engine_warning.png"
                    anchors.verticalCenterOffset: 60
                    fillMode: Image.PreserveAspectFit
                }

                Image {
                    id: waterTempStatus
                    x: 94
                    y: 96
                    width: 64
                    height: 53
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    source: "water_temp_normal.png"
                    anchors.verticalCenterOffset: 60
                    fillMode: Image.PreserveAspectFit
                }

                Image {
                    id: oilPressureStatus
                    x: 164
                    y: 102
                    width: 53
                    height: 47
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenterOffset: 80
                    anchors.horizontalCenter: parent.horizontalCenter
                    source: "oil_pres_warning.png"
                    anchors.verticalCenterOffset: 60
                    fillMode: Image.PreserveAspectFit
                }

                StatusIndicator {
                    id: coolantFanState
                    x: 37
                    y: 32
                    width: 35
                    height: 35
                    anchors.verticalCenterOffset: -40
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenterOffset: -80
                    anchors.horizontalCenter: parent.horizontalCenter
                    color: Qt.rgba(0 , 255, 0, 0.5)

                    Label {
                        id: cltStatuslabel
                        x: -11
                        color: "#bdbebf"
                        text: qsTr("CLT FAN ")
                        anchors.top: parent.bottom
                        anchors.horizontalCenterOffset: 0
                        anchors.horizontalCenter: parent.horizontalCenter
                        verticalAlignment: Text.AlignVCenter
                        anchors.topMargin: 10
                        horizontalAlignment: Text.AlignHCenter
                    }
                }

                StatusIndicator {
                    id: fuelPumpState
                    x: 217
                    y: 32
                    width: 35
                    height: 35
                    color: "#8000ff00"
                    anchors.verticalCenterOffset: -40
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenterOffset: 80
                    anchors.horizontalCenter: parent.horizontalCenter

                    Label {
                        id: fuelPumpStateLabel
                        x: 2
                        color: "#bdbebf"
                        text: qsTr("FUEL PUMP")
                        anchors.top: parent.bottom
                        verticalAlignment: Text.AlignVCenter
                        anchors.topMargin: 10
                        horizontalAlignment: Text.AlignHCenter
                        anchors.horizontalCenterOffset: 0
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }


            }

            Item {
                id: safety
                width: 243
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.bottom: parent.bottom
                anchors.horizontalCenterOffset: secondaryOverview.width > 1300 ? (-secondaryOverview.width/3 + width/2) : (-secondaryOverview.width/3)
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottomMargin: 0

                Text {
                    id: safety_text
                    x: 299
                    y: 8
                    color: "#bdbebf"
                    text: qsTr("SAFETY")
                    anchors.top: parent.top
                    anchors.topMargin: 8
                    anchors.horizontalCenter: parent.horizontalCenter
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: 15
                }

                StatusIndicator {
                    id: bspdState
                    width: 35
                    height: 35
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenterOffset: -75
                    anchors.verticalCenterOffset: -40
                    anchors.horizontalCenter: parent.horizontalCenter

                    Label {
                        id: bspdLabel
                        x: 0
                        width: 26
                        height: 10
                        color: "#bdbebf"
                        text: qsTr("BSPD")
                        anchors.top: parent.bottom
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        anchors.topMargin: 10
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }

                StatusIndicator {
                    id: cockpitState
                    width: 35
                    height: 35
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenterOffset: 60
                    anchors.horizontalCenterOffset: 0
                    Label {
                        id: cockpitLabel
                        x: 0
                        width: 34
                        height: 13
                        color: "#bdbebf"
                        text: qsTr("Cockpit")
                        anchors.top: parent.bottom
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.topMargin: 10
                    }
                }

                StatusIndicator {
                    id: leftState
                    width: 35
                    height: 35
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenterOffset: 60
                    anchors.horizontalCenterOffset: -75
                    Label {
                        id: leftLabel
                        x: 0
                        width: 20
                        height: 15
                        color: "#bdbebf"
                        text: qsTr("Left")
                        anchors.top: parent.bottom
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.topMargin: 10
                    }
                }

                StatusIndicator {
                    id: rightState
                    width: 35
                    height: 35
                    anchors.verticalCenter: parent.verticalCenter
                    active: false
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenterOffset: 60
                    anchors.horizontalCenterOffset: 75
                    Label {
                        id: rightLabel
                        x: 0
                        width: 34
                        height: 13
                        color: "#bdbebf"
                        text: qsTr("Right")
                        anchors.top: parent.bottom
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.topMargin: 10
                    }
                }

                StatusIndicator {
                    id: botsState
                    width: 35
                    height: 35
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenterOffset: -40
                    anchors.horizontalCenterOffset: 0
                    Label {
                        id: botsLabel
                        x: 0
                        width: 26
                        height: 10
                        color: "#bdbebf"
                        text: qsTr("BOTS")
                        anchors.top: parent.bottom
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.topMargin: 10
                    }
                }

                StatusIndicator {
                    id: inertiaSwitchState
                    width: 35
                    height: 35
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenterOffset: -40
                    anchors.horizontalCenterOffset: 75
                    Label {
                        id: inertiaSwitchLabel
                        x: 0
                        width: 26
                        height: 10
                        color: "#bdbebf"
                        text: qsTr("Inertia")
                        anchors.top: parent.bottom
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.topMargin: 10
                    }
                }
            }
        }





        Item {
            id: mainOverview
            height: 300
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 0
            anchors.topMargin: 0
            anchors.rightMargin: 0
            anchors.bottomMargin: rectangle.height/3


            Gauge {
                id: throttleGauge
                width: 40
                height: 200
                scale: 1
                anchors.horizontalCenterOffset: 0
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 20
                anchors.horizontalCenter: parent.horizontalCenter
                rotation: 90
                tickmarkStepSize: 0

                Behavior on value {
                    NumberAnimation {
                        duration: 100
                    }
                }

                style: GaugeStyle {
                    valueBar: Rectangle {
                        color: Qt.rgba(0 , 1, 0, 0.5)
                        implicitWidth: 16
                    }
                }

                minimumValue: 0
                value: tps.value
                maximumValue: 100
                Label {
                    id: throttleLabel
                    x: 0
                    y: 62
                    color: "#bdbebf"
                    text: qsTr("THROTTLE")
                    anchors.verticalCenterOffset: 0
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: -10
                    rotation: -90
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            Gauge {
                id: brakeGauge
                width: 40
                height: 170
                anchors.horizontalCenterOffset: 0
                anchors.bottom: parent.bottom
                anchors.bottomMargin: -10
                anchors.horizontalCenter: parent.horizontalCenter
                rotation: 90
                tickmarkStepSize: 0

                Behavior on value {
                    NumberAnimation {
                        duration: 1000
                    }
                }

                style: GaugeStyle {
                    valueBar: Rectangle {
                        color: Qt.rgba(1 , 0, 0, 0.5)
                        implicitWidth: 16
                    }
                }
                minimumValue: 0
                value: brake.value
                maximumValue: 100
                Label {
                    id: brakeLabel
                    color: "#bdbebf"
                    text: qsTr("BRAKE")
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: 0
                    rotation: -90
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            CircularGauge {
                id: rpmGauge
                value: parseInt(rpm_gauge.value)/100
                maximumValue: 150
                anchors.left: parent.left
                anchors.leftMargin: 189
                anchors.right: parent.right
                anchors.rightMargin: 190
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 120

                style: CircularGaugeStyle {

                    function degreesToRadians(degrees) {
                        return degrees * (Math.PI / 180);
                    }

                    background: Canvas {
                        onPaint: {
                            var ctx = getContext("2d");
                            ctx.reset();

                            ctx.beginPath();
                            ctx.strokeStyle = "#e34c22";
                            ctx.lineWidth = outerRadius * 0.02;

                            ctx.arc(outerRadius, outerRadius, outerRadius - ctx.lineWidth / 2,
                                    degreesToRadians(valueToAngle(130) - 90), degreesToRadians(valueToAngle(150) - 90));
                            ctx.stroke();
                        }
                    }

                    tickmark: Rectangle {
                        color: styleData.value >= 130 ? "#e34c22" : "#e5e5e5"
                        implicitWidth: outerRadius * 0.02
                        visible: styleData.value < 130 || styleData.value % 10 == 0
                        implicitHeight: outerRadius * 0.06
                        antialiasing: true
                    }

                    tickmarkLabel: Text {
                        color: styleData.value >= 130 ? "#e34c22" : "#e5e5e5"
                        text: styleData.value
                        font.pixelSize: Math.max(6, outerRadius * 0.1)
                        antialiasing: true
                    }
                    minorTickmark: Rectangle {
                        color: "#e5e5e5"
                        implicitWidth: outerRadius * 0.01
                        visible: styleData.value < 130
                        implicitHeight: outerRadius * 0.03
                        antialiasing: true
                    }
                }

                Label {
                    id: rpmMultiplier1
                    color: "#bdbebf"
                    text: qsTr("RPM x100")
                    anchors.verticalCenterOffset: -40
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            Gauge {
                id: oilTmpGauge
                x: 575
                y: 10
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.top: parent.top
                clip: false
                anchors.bottomMargin: 20
                anchors.margins: 10
                baselineOffset: 0
                z: 0

                Behavior on value {
                    NumberAnimation {
                        duration: 1000
                    }
                }

                style: GaugeStyle {
                    valueBar: Rectangle {
                        color: Qt.rgba(oilTmpGauge.value / oilTmpGauge.maximumValue, 0, 1 - oilTmpGauge.value / oilTmpGauge.maximumValue, 1)
                        implicitWidth: 16
                    }
                }

                value: oil_tmp.value
                maximumValue: 130
                Label {
                    id: oilTmpLabel
                    y: 271
                    height: 16
                    color: "#bdbebf"
                    text: qsTr("OILT")
                    anchors.bottomMargin: -15
                    anchors.leftMargin: 0
                    verticalAlignment: Text.AlignVCenter
                    anchors.right: parent.right
                    anchors.left: parent.left
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            CircularGauge {
                id: oilPressureGauge
                anchors.top: rpmGauge.verticalCenter
                anchors.topMargin: 100
                anchors.left: rpmGauge.horizontalCenter
                anchors.leftMargin: 100
                anchors.right: oilTmpGauge.left
                anchors.rightMargin: 6
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                value: oil_pressure.value
                maximumValue: 10

                Behavior on value {
                    NumberAnimation {
                        duration: 1000
                    }
                }

                style: CircularGaugeStyle {

                    function degreesToRadians(degrees) {
                        return degrees * (Math.PI / 180);
                    }

                    background: Canvas {
                        onPaint: {
                            var ctx = getContext("2d");
                            ctx.reset();

                            ctx.beginPath();
                            ctx.strokeStyle = "#e34c22";
                            ctx.lineWidth = outerRadius * 0.02;

                            ctx.arc(outerRadius, outerRadius, outerRadius - ctx.lineWidth / 2,
                                    degreesToRadians(valueToAngle(8) - 90), degreesToRadians(valueToAngle(10) - 90));
                            ctx.stroke();
                        }
                    }

                    minorTickmarkCount : 4
                    tickmarkStepSize: 1

                    tickmark: Rectangle {
                        color: styleData.value >= 8 ? "#e34c22" : "#e5e5e5"
                        implicitWidth: outerRadius * 0.02
                        visible: styleData.value < 8 || styleData.value % 1 == 0
                        implicitHeight: outerRadius * 0.06
                        antialiasing: true
                    }

                    tickmarkLabel: Text {
                        color: styleData.value >= 8 ? "#e34c22" : "#e5e5e5"
                        text: styleData.value
                        font.pixelSize: Math.max(6, outerRadius * 0.1)
                        antialiasing: true
                    }
                    minorTickmark: Rectangle {
                        color: "#e5e5e5"
                        visible: styleData.value < 8
                        implicitWidth: outerRadius * 0.01
                        implicitHeight: outerRadius * 0.03
                        antialiasing: true
                    }
                }

                Label {
                    id: oilPressureLabel
                    color: "#bdbebf"
                    text: qsTr("OILP")
                    anchors.verticalCenterOffset: -30
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            Gauge {
                id: cltGauge
                x: 10
                y: 10
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.bottomMargin: 20
                anchors.margins: 10

                Behavior on value {
                    NumberAnimation {
                        duration: 1000
                    }
                }

                style: GaugeStyle {
                    valueBar: Rectangle {
                        color: Qt.rgba(cltGauge.value / cltGauge.maximumValue, 0, 1 - cltGauge.value / cltGauge.maximumValue, 1)
                        implicitWidth: 16
                    }
                }
                value: coolant_tmp.value
                maximumValue: 130
                Label {
                    id: cltLabel
                    y: 271
                    height: 16
                    color: "#bdbebf"
                    text: qsTr("CLT")
                    anchors.bottomMargin: -15
                    anchors.leftMargin: 0
                    verticalAlignment: Text.AlignVCenter
                    anchors.right: parent.right
                    anchors.left: parent.left
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            Label {
                id: speedValue
                x: 134
                y: -86
                width: 19
                height: 27
                color: "#bdbebf"
                text: qsTr("0")
                anchors.horizontalCenterOffset: -30
                anchors.horizontalCenter: fuelPressureGauge.horizontalCenter
                anchors.verticalCenterOffset: 0
                anchors.verticalCenter: rpmGauge.verticalCenter
                verticalAlignment: Text.AlignVCenter
                font.pointSize: 12
                horizontalAlignment: Text.AlignHCenter

                Label {
                    id: label1
                    x: 8
                    y: 27
                    color: "#bdbebf"
                    text: qsTr("SPEED")
                    anchors.verticalCenterOffset: -20
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            CircularGauge {
                id: fuelPressureGauge
                anchors.top: rpmGauge.verticalCenter
                anchors.topMargin: 100
                anchors.right: rpmGauge.horizontalCenter
                anchors.rightMargin: 100
                anchors.left: cltGauge.right
                anchors.leftMargin: 6
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                value: fuel_pressure.value
                maximumValue: 5



                Behavior on value {
                    NumberAnimation {
                        duration: 1000
                    }
                }

                style: CircularGaugeStyle {

                    function degreesToRadians(degrees) {
                        return degrees * (Math.PI / 180);
                    }

                    background: Canvas {
                        onPaint: {
                            var ctx = getContext("2d");
                            ctx.reset();

                            ctx.beginPath();
                            ctx.strokeStyle = "#e34c22";
                            ctx.lineWidth = outerRadius * 0.02;

                            ctx.arc(outerRadius, outerRadius, outerRadius - ctx.lineWidth / 2,
                                    degreesToRadians(valueToAngle(4) - 90), degreesToRadians(valueToAngle(5) - 90));
                            ctx.stroke();
                        }
                    }

                    minorTickmarkCount : 4
                    tickmarkStepSize: 0.5

                    tickmark: Rectangle {
                        color: styleData.value >= 4 ? "#e34c22" : "#e5e5e5"
                        implicitWidth: outerRadius * 0.02
                        visible: styleData.value <= 4 || styleData.value % 1 == 0
                        implicitHeight: outerRadius * 0.06
                        antialiasing: true
                    }


                    tickmarkLabel: Text {
                        color: styleData.value >= 4 ? "#e34c22" : "#e5e5e5"
                        text: styleData.value
                        font.pixelSize: Math.max(6, outerRadius * 0.1)
                        antialiasing: true
                    }
                    minorTickmark: Rectangle {
                        color: "#e5e5e5"
                        visible: styleData.value < 4
                        implicitWidth: outerRadius * 0.01
                        implicitHeight: outerRadius * 0.03
                        antialiasing: true
                    }
                }

                Label {
                    id: fuelPressureLabel
                    color: "#bdbebf"
                    text: qsTr("FUELP")
                    anchors.verticalCenterOffset: -30
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            Label {
                id: gearValue
                x: 491
                y: 86
                width: 20
                color: "#bdbebf"
                text: "N"
                anchors.horizontalCenterOffset: 30
                anchors.horizontalCenter: oilPressureGauge.horizontalCenter
                anchors.verticalCenter: rpmGauge.verticalCenter
                verticalAlignment: Text.AlignVCenter
                font.pointSize: 12
                horizontalAlignment: Text.AlignHCenter

                Label {
                    id: label
                    x: 8
                    y: 9
                    color: "#bdbebf"
                    text: qsTr("GEAR")
                    anchors.verticalCenterOffset: -20
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            Slider {
                id: slider
                x: 0
                y: 480
                anchors.bottom: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                wheelEnabled: false
                to: 150
                value: 0
                from: -50
            }

            Rectangle {
                id: line
                x: 97
                y: 272
                width: mainOverview.width
                height: 1
                color: "#bdbebf"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                anchors.horizontalCenter: parent.horizontalCenter
            }

        }


    }
}




