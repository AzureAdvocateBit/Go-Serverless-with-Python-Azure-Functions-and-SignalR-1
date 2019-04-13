from azure.cosmosdb.table.tableservice import TableService

class Calibrate():

    def __init__(self, table_service, calibrationTable, partitionKey):
        this.calibrationDictionary = {}
        this.table_service = table_service
        this.calibrationTable = calibrationTable
        this.partitionKey = partitionKey

        if not table_service.exists(calibrationTable):
            table_service.create_table(calibrationTable)

    def calibrateTelemetry(self, telemetry):
        calibrationData = getCalibrationData(
            telemetry.get('deviceId', telemetry.get('DeviceId')))

        if calibrationData is not None:
            telemetry["Celsius"] = calibrate(
                telemetry.get("Celsius"), calibrationData.get("TemperatureSlope"), calibrationData.get("TemperatureYIntercept"))
            telemetry["Humidity"] = calibrate(
                telemetry.get("Humidity"), calibrationData.get("HumiditySlope"), calibrationData.get("HumidityYIntercept"))
            telemetry["hPa"] = calibrate(
                telemetry.get("hPa"), calibrationData.get("PressureSlope"), calibrationData.get("PressureYIntercept"))


    def calibrate(self, value, slope, intercept):
        if value is None or slope is None or intercept is None:
            return value
        return value * slope + intercept


    def getCalibrationData(self, deviceId):
        if deviceId not in self.calibrationDictionary:
            try:
                self.calibrationDictionary[deviceId] = self.table_service.get_entity(
                    self.calibrationTable, self.partitionKey, deviceId)
            except:
                self.calibrationDictionary[deviceId] = None

        return self.calibrationDictionary[deviceId]
