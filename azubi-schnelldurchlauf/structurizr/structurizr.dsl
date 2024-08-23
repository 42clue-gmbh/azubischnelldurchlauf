workspace {
    model {
        customer = person "Customer"

        temprature = softwareSystem "Temperature Monitor" {
            tags = "Primary"
            grafana = container "Grafana"{
                tags = "Web"
            }
            influxdb = container "InfluxDB"{
                tags = "Database"
            }
            weather = container "Weather"{
                tags = "Primary"
                weather_main = component "main"
                weather_get = component "get_data"
                weather_process = component "process_data"
                weather_store = component "store_data"
            }
        }

        temperature_sensor = softwareSystem "Temperature Sensor"{
            tags = "Extern"
        }

        customer -> grafana "Uses"
        grafana -> influxdb "Reads from"

        weather_store -> influxdb "Writes to"
        weather_process -> weather_store ""
        weather_get -> weather_process ""
        
        weather_main -> weather_get "Orchestrates"
        weather_main -> weather_process "Orchestrates"
        weather_main -> weather_store "Orchestrates"

        weather_get -> temperature_sensor "Reads from"
    }

    views {
        systemContext temprature "systemContext" {
            include *
            autolayout lr
        }

        container temprature "container" {
            include *
            autolayout lr
        }

        component weather "component" {
            include *
            autolayout lr
        }

        styles {
            element "Person" {
                background #c7d7db

                color #1d1d1b
                shape Person
            }

            element "Database" {
                background #03344A
                color #f5f5ee
                shape Cylinder
            }

            element "Web" {
                background #03344A
                color #f5f5ee
                //shape WebBrowser

            }

            element "Primary" {
                background #0074a4
                color #f5f5ee
            }
            element "Extern" {
                background #5c6466
                color #f5f5ee
            }
        }
    }
}

// night blue #03344A
// neon yellow #ffff00
// silbergrau #8A9597
// cremeweiss v2 #f5f5ee
// cremeweiss v2.1 #f3f3e9
// blue #0074a4
// pastel blue #c3e7f6
// hell neongelb #f8ffaf
// hell silbergrau #c7d7db
// dunkel silbergrau #5c6466
// schwarz #1d1d1b

// SCHRIFT
// schwarz #1d1d1b
// cremeweiss v2 #f5f5ee
