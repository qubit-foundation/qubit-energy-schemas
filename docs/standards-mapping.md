# Standards Mapping

This document maps Qubit Energy schemas to existing industry standards, enabling interoperability with established energy data protocols and specifications.

## Overview

The Qubit Energy schemas are designed to complement, not replace, existing energy industry standards. Our approach:

1. **Compatibility**: Maintain compatibility with widely adopted standards
2. **Translation**: Provide clear mappings between schema fields and standard attributes
3. **Extension**: Extend standards where needed for modern energy systems
4. **Bridging**: Enable systems to work with multiple standards simultaneously

## IEC 61850 - Power Systems Communication

IEC 61850 is the international standard for communication protocols in electrical substations.

### Asset Mapping

| Qubit Schema | IEC 61850 Logical Node | Description |
|--------------|------------------------|-------------|
| `asset.type: solar_pv` | `DPOW` | Distributed Power Resource |
| `asset.type: battery_storage` | `ZBAT` | Battery System |
| `asset.type: wind_turbine` | `WTUR` | Wind Turbine |
| `asset.type: transformer` | `YPTR` | Power Transformer |
| `asset.type: grid_connection` | `XCBR` | Circuit Breaker |

### Measurement Mapping

| Qubit Schema | IEC 61850 CDC | Data Attribute | Unit |
|--------------|---------------|----------------|------|
| `meter.active_power` | `MV` | `mag.f` | W |
| `meter.reactive_power` | `MV` | `mag.f` | VAr |
| `meter.voltage` | `MV` | `mag.f` | V |
| `meter.current` | `MV` | `mag.f` | A |
| `meter.frequency` | `MV` | `mag.f` | Hz |

### Communication Integration

```json
{
  "asset": {
    "control_system": {
      "protocol": "iec61850",
      "logical_device": "SOLAR_LD01",
      "logical_node": "DPOW1",
      "data_objects": {
        "TotW": "active_power",
        "TotVAr": "reactive_power",
        "Vol": "voltage"
      }
    }
  }
}
```

## OCPP 2.0.1 - EV Charging Protocol

Open Charge Point Protocol for electric vehicle charging stations.

### Asset Type Mapping

| Qubit Schema | OCPP Component | Connector Type |
|--------------|----------------|----------------|
| `asset.type: ev_charger` | `ChargingStation` | Various |
| `asset.subtype: ac_level_1` | `EVSE` | `cType1` |
| `asset.subtype: ac_level_2` | `EVSE` | `cType2` |
| `asset.subtype: dc_fast` | `EVSE` | `cCCS1/cCCS2` |

### Meter Integration

```json
{
  "meter": {
    "type": "ev_charger",
    "ocpp_config": {
      "charge_point_id": "CP001",
      "connector_id": 1,
      "measurand": "Energy.Active.Import.Register",
      "phase": "L1-N",
      "location": "Outlet",
      "unit": "kWh"
    }
  }
}
```

### Transaction Data

| Qubit Schema | OCPP Message | Field |
|--------------|--------------|-------|
| `timeseries.energy` | `MeterValues` | `Energy.Active.Import.Register` |
| `timeseries.power` | `MeterValues` | `Power.Active.Import` |
| `sensor.temperature` | `MeterValues` | `Temperature` |

## OpenADR 2.0 - Demand Response

Open Automated Demand Response standard for grid flexibility.

### Site Mapping

| Qubit Schema | OpenADR | Description |
|--------------|---------|-------------|
| `site.id` | `venID` | Virtual End Node Identifier |
| `site.organization_id` | `vtnID` | Virtual Top Node Identifier |
| `asset.capacity.power_kw` | `resourceID` | Demand Response Resource |

### Event Integration

```json
{
  "event": {
    "type": "demand_response",
    "opendr_event": {
      "event_id": "DR_EVENT_001",
      "market_context": "CAISO",
      "event_status": "active",
      "test_event": false,
      "vtn_comment": "Peak demand reduction"
    },
    "targets": [
      {
        "site_id": "sit_solar_farm_01",
        "reduction_kw": 5000,
        "duration_minutes": 120
      }
    ]
  }
}
```

## IEEE 2030.5 - Smart Energy Profile

Standard for smart grid end device communications.

### Device Information

| Qubit Schema | IEEE 2030.5 | Resource |
|--------------|-------------|----------|
| `asset.manufacturer_info` | `DeviceInformation` | `/dcap/di` |
| `meter.measurements` | `MirrorMeterReading` | `/mup/mirr` |
| `site.energy_profile` | `DemandResponseProgram` | `/dr` |

### Time Series Data

```json
{
  "timeseries": {
    "ieee_2030_5": {
      "reading_type": {
        "uom": 72,
        "powerOfTenMultiplier": 3,
        "kind": 12,
        "phase": "s12n"
      },
      "interval_reading": {
        "cost": null,
        "value": 45000,
        "reading_quality": 0
      }
    }
  }
}
```

## CIMXML - Common Information Model

IEC 61970/61968 standards for power system model exchange.

### Equipment Mapping

| Qubit Schema | CIM Class | Package |
|--------------|-----------|---------|
| `asset.type: solar_pv` | `PhotovoltaicUnit` | `Generation.Production` |
| `asset.type: battery_storage` | `BatteryUnit` | `Generation.Production` |
| `site` | `Substation` | `Core.Substation` |
| `organization` | `Company` | `Common.Organization` |

### Geographic Information

```xml
<cim:Location rdf:ID="LOC_SITE_001">
  <cim:Location.CoordinateSystem>WGS84</cim:Location.CoordinateSystem>
  <cim:PositionPoint.Location rdf:resource="#LOC_SITE_001"/>
  <cim:PositionPoint.sequenceNumber>1</cim:PositionPoint.sequenceNumber>
  <cim:PositionPoint.xPosition>-122.4194</cim:PositionPoint.xPosition>
  <cim:PositionPoint.yPosition>37.7749</cim:PositionPoint.yPosition>
</cim:Location>
```

## Energy Star Portfolio Manager

EPA's tool for tracking building energy performance.

### Site Mapping

| Qubit Schema | Portfolio Manager | API Field |
|--------------|-------------------|-----------|
| `site.type: commercial_building` | Property Type | `propertyUse` |
| `site.area_m2` | Gross Floor Area | `grossFloorArea` |
| `site.energy_profile.annual_consumption_kwh` | Energy Use | `energyUse` |

### Meter Configuration

```json
{
  "meter": {
    "type": "main",
    "portfolio_manager": {
      "property_id": 12345678,
      "meter_id": 87654321,
      "meter_type": "Electric",
      "units": "kWh (thousand Watt-hours)"
    }
  }
}
```

## NAESB REQ.21 - Energy Services Provider Interface

North American Energy Standards Board wholesale market standards.

### Market Participant

| Qubit Schema | NAESB | Description |
|--------------|-------|-------------|
| `organization.type: utility` | Load Serving Entity | LSE |
| `organization.type: ipp` | Qualified Scheduling Entity | QSE |
| `site.grid_connection.utility` | Transmission Service Provider | TSP |

## Green Button Data

Standard for utility customer energy usage data.

### Usage Point Mapping

| Qubit Schema | Green Button | Description |
|--------------|--------------|-------------|
| `meter.id` | `UsagePoint.mRID` | Meter Resource ID |
| `timeseries.measurement.parameter` | `ReadingType.kind` | Measurement Kind |
| `timeseries.measurement.unit` | `ReadingType.uom` | Unit of Measure |

### Interval Data

```json
{
  "timeseries": {
    "green_button": {
      "usage_point": "met_main_revenue_01",
      "reading_type": {
        "kind": "energy",
        "uom": "Wh",
        "powerOfTenMultiplier": 3,
        "timeAttribute": 0,
        "intervalLength": 900
      }
    }
  }
}
```

## MODBUS Protocol Mapping

Industrial communication standard widely used in energy systems.

### Register Mapping

| Measurement | Modbus Function | Register Type | Data Type |
|-------------|-----------------|---------------|-----------|
| Active Power | 03 (Read Holding) | Holding | FLOAT32 |
| Energy | 04 (Read Input) | Input | UINT32 |
| Voltage | 04 (Read Input) | Input | FLOAT32 |
| Current | 04 (Read Input) | Input | FLOAT32 |

### Device Configuration

```json
{
  "meter": {
    "communication": {
      "protocol": "modbus_rtu",
      "address": 1,
      "baud_rate": 9600,
      "parity": "none",
      "stop_bits": 1,
      "registers": {
        "active_power": {"address": 30001, "type": "holding", "format": "float32"},
        "energy": {"address": 30003, "type": "holding", "format": "uint32"},
        "voltage": {"address": 30005, "type": "input", "format": "float32"}
      }
    }
  }
}
```

## Translation Guidelines

### Data Type Conversion

| Qubit Type | Standard Types |
|------------|----------------|
| `timestamp` | Unix epoch, ISO 8601, Timestamp |
| `measurement_unit` | IEC unit symbols, UCUM codes |
| `location` | WGS84 coordinates, UTM, local grid |
| `status` | Various enumeration mappings |

### Identifier Mapping

Create consistent identifier mappings:

```json
{
  "external_identifiers": {
    "iec_61850": "SOLAR_FARM_01>>DPOW1",
    "ocpp": "CP_SF01_01",
    "scada": "PV_UNIT_001",
    "utility": "METER_12345678"
  }
}
```

### Implementation Examples

#### Multi-Standard Integration

```python
class EnergyDataTranslator:
    def to_iec61850(self, qubit_data):
        # Convert Qubit schema to IEC 61850 format
        pass
    
    def to_ocpp(self, qubit_data):
        # Convert to OCPP message format
        pass
    
    def from_modbus(self, modbus_data):
        # Convert Modbus data to Qubit schema
        pass
```

## Future Standards Integration

### Planned Additions

- **Matter/Thread**: IoT device interoperability
- **OCPI**: EV roaming protocol
- **IEC 62325**: Market communications
- **NAESB WEQ**: Wholesale electric quadrant standards
- **NIST Framework**: Cybersecurity framework mapping

### Contributing Standards Mappings

1. Identify standard and use case
2. Create mapping table
3. Provide example translations  
4. Test with real data
5. Submit pull request with documentation

This living document grows with community contributions and new standard adoptions.