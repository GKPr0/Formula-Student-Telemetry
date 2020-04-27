import QtQuick 2.12
import QtQuick.Extras 1.4
import QtQuick.Controls 2.3
import QtQuick.Controls.Styles 1.4

Item {

    Connections {
        target: slider
        onValueChanged: {
            rpmGauge.value = slider.value
            cltGauge.value = slider.value
            oilTmpGauge.value = slider.value
            oilPressureGauge.value = slider.value
            fuelPressureGauge.value = slider.value
        }
    }

    Rectangle {
        id: rectangle
        color: "#4f4e4e"
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        anchors.fill: parent

        Slider {
            id: slider
            anchors.left: parent.left
            anchors.leftMargin: 213
            anchors.right: parent.right
            anchors.rightMargin: 227
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 15
            anchors.top: rpmGauge.bottom
            anchors.topMargin: 163
            wheelEnabled: false
            to: 150
            value: 0
        }

        CircularGauge {
            id: rpmGauge
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.topMargin: 33
            anchors.rightMargin: 192
            anchors.bottomMargin: 224
            anchors.leftMargin: 177
            enabled: false
            value: rpm_gauge.value
            maximumValue: 150

            style: CircularGaugeStyle {
                id: style

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
                    visible: styleData.value < 130 || styleData.value % 10 == 0
                    implicitWidth: outerRadius * 0.02
                    antialiasing: true
                    implicitHeight: outerRadius * 0.06
                    color: styleData.value >= 130 ? "#e34c22" : "#e5e5e5"
                }

                minorTickmark: Rectangle {
                    visible: styleData.value < 130
                    implicitWidth: outerRadius * 0.01
                    antialiasing: true
                    implicitHeight: outerRadius * 0.03
                    color: "#e5e5e5"
                }

                tickmarkLabel:  Text {
                    font.pixelSize: Math.max(6, outerRadius * 0.1)
                    text: styleData.value
                    color: styleData.value >= 130 ? "#e34c22" : "#e5e5e5"
                    antialiasing: true
                }
            }

            Label {
                id: rpmMultiplier
                text: qsTr("RPM x100")
                anchors.top: parent.top
                anchors.topMargin: 66
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 147
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.right: parent.right
                anchors.rightMargin: 107
                anchors.left: parent.left
                anchors.leftMargin: 107
            }
        }

        Label {
            id: gearValue
            color: "#bdbebf"
            text: gear.value
            font.pointSize: 12
            anchors.left: rpmGauge.left
            anchors.right: rpmGauge.right
            anchors.bottom: rpmGauge.bottom
            anchors.top: rpmGauge.bottom
            anchors.leftMargin: 120
            anchors.topMargin: 13
            anchors.rightMargin: 120
            anchors.bottomMargin: -40
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
        }

        Gauge {
            id: cltGauge
            value: coolant_tmp.value
            anchors.right: oilTmpGauge.left
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.top: parent.top
            maximumValue: 120
            anchors.rightMargin: 29
            anchors.bottomMargin: 224
            anchors.leftMargin: 30
            anchors.topMargin: 33
            anchors.margins: 10

            Behavior on value {
                NumberAnimation {
                    duration: 1000
                }
            }

            style: GaugeStyle {
                valueBar: Rectangle {
                    implicitWidth: 16
                    color: Qt.rgba(cltGauge.value / cltGauge.maximumValue, 0, 1 - cltGauge.value / cltGauge.maximumValue, 1)
                }
            }

            Label {
                id: cltLabel
                y: 224
                height: 16
                color: "#bdbebf"
                text: qsTr("CLT")
                anchors.bottom: parent.bottom
                anchors.bottomMargin: -17
                anchors.left: parent.left
                anchors.leftMargin: 8
                anchors.right: parent.right
                anchors.rightMargin: 7
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }

        Gauge {
            id: oilTmpGauge
            value: oil_tmp.value
            anchors.left: parent.left
            anchors.right: rpmGauge.left
            anchors.bottom: parent.bottom
            anchors.top: parent.top
            maximumValue: 120
            anchors.rightMargin: 6
            anchors.bottomMargin: 224
            anchors.leftMargin: 115
            anchors.topMargin: 33
            anchors.margins: 10

            Behavior on value {
                NumberAnimation {
                    duration: 1000
                }
            }

            style: GaugeStyle {
                valueBar: Rectangle {
                    implicitWidth: 16
                    color: Qt.rgba(oilTmpGauge.value / oilTmpGauge.maximumValue, 0, 1 - oilTmpGauge.value / oilTmpGauge.maximumValue, 1)
                }
            }

            Label {
                id: oilTmpLabel
                y: 224
                height: 16
                color: "#bdbebf"
                text: qsTr("OILT")
                anchors.bottom: parent.bottom
                anchors.bottomMargin: -17
                anchors.right: parent.right
                anchors.rightMargin: 7
                anchors.left: parent.left
                anchors.leftMargin: 8
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }

        Gauge {
            id: oilPressureGauge
            value: oil_pressure.value
            anchors.left: rpmGauge.right
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.top: parent.top
            maximumValue: 20
            anchors.rightMargin: 130
            anchors.bottomMargin: 224
            anchors.leftMargin: 6
            anchors.topMargin: 33
            anchors.margins: 10

            Behavior on value {
                NumberAnimation {
                    duration: 1000
                }
            }

            style: GaugeStyle {
                valueBar: Rectangle {
                    implicitWidth: 16
                    color: Qt.rgba(oilPressureGauge.value / oilPressureGauge.maximumValue, 0, 1 - oilPressureGauge.value / oilPressureGauge.maximumValue, 1)
                }
            }

            Label {
                id: oilPressureLabel
                y: 224
                height: 16
                color: "#bdbebf"
                text: qsTr("OILP")
                anchors.bottom: parent.bottom
                anchors.bottomMargin: -17
                anchors.left: parent.left
                anchors.leftMargin: 8
                anchors.right: parent.right
                anchors.rightMargin: 7
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }

        Gauge {
            id: fuelPressureGauge
            value: fuel_pressure.value
            anchors.left: oilPresureGauge.right
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.top: parent.top
            maximumValue: 20
            anchors.rightMargin: 31
            anchors.bottomMargin: 224
            anchors.leftMargin: 42
            anchors.topMargin: 33
            anchors.margins: 10

            Behavior on value {
                NumberAnimation {
                    duration: 1000
                }
            }

            style: GaugeStyle {
                valueBar: Rectangle {
                    implicitWidth: 16
                    color: Qt.rgba(fuelPressureGauge.value / fuelPressureGauge.maximumValue, 0, 1 - fuelPressureGauge.value / fuelPressureGauge.maximumValue, 1)
                }
            }

            Label {
                id: fuelPressureLabel
                y: 224
                height: 16
                color: "#bdbebf"
                text: qsTr("FUELP")
                anchors.bottom: parent.bottom
                anchors.bottomMargin: -17
                anchors.left: parent.left
                anchors.leftMargin: 8
                anchors.right: parent.right
                anchors.rightMargin: 7
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }

        Label {
            id: flDumper
            text: fl_dumper.value
            x: 43
            width: 11
            height: 24
            color: "#bdbebf"
            anchors.top: suspensionFrame.top
            anchors.topMargin: 23
            anchors.right: suspensionFrame.left
            anchors.rightMargin: 11
            font.pointSize: 12
        }

        Label {
            id: frDumper
            text: fr_dumper.value
            width: 11
            height: 22
            color: "#bdbebf"

            anchors.top: suspensionFrame.top
            anchors.topMargin: 24
            anchors.left: suspensionFrame.right
            anchors.leftMargin: 12
            font.pointSize: 12
        }

        Label {
            id: rlDumper
            text: rl_dumper.value
            x: 43
            color: "#bdbebf"
            anchors.top: suspensionFrame.top
            anchors.topMargin: 89
            anchors.right: suspensionFrame.left
            anchors.rightMargin: 11
            font.pointSize: 12
        }

        Label {
            id: rrDumper
            text: rr_dumper.value
            color: "#bdbebf"
            anchors.top: suspensionFrame.top
            anchors.topMargin: 89
            anchors.left: suspensionFrame.right
            anchors.leftMargin: 12
            font.pointSize: 12
        }

        Frame {
            id: suspensionFrame
            anchors.right: slider.left
            anchors.rightMargin: 57
            anchors.top: rpmGauge.bottom
            anchors.topMargin: 80
            anchors.left: parent.left
            anchors.leftMargin: 65
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0

            Label {
                id: suspensionlabel
                height: 16
                color: "#bdbebf"
                text: qsTr("Suspension")
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.top: parent.top
                anchors.topMargin: -12
                anchors.right: parent.right
                anchors.rightMargin: 12
                anchors.left: parent.left
                anchors.leftMargin: 12
            }
        }

        Frame {
            id: safetyFrame
            anchors.left: slider.right
            anchors.leftMargin: 27
            anchors.top: rpmGauge.bottom
            anchors.topMargin: 64
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            anchors.right: parent.right
            anchors.rightMargin: 0

            Label {
                id: safetylabel
                x: 70
                y: -12
                color: "#bdbebf"
                text: qsTr("Safety")
            }
        }




    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
