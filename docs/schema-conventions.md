# Schema Design Conventions

This document defines the design principles, naming conventions, and technical standards for Qubit Energy Schemas.

## Core Principles

1. **Simplicity**: Start minimal, extend as needed
2. **Clarity**: Self-documenting with descriptions
3. **Consistency**: Uniform patterns across all schemas
4. **Interoperability**: Compatible with industry standards
5. **Extensibility**: Support custom fields without breaking changes

## Naming Conventions

### Schema Files
- Use snake_case: `organization.json`, `time_series.json`
- Version in path: `schemas/v0.1/asset.json`
- Descriptive names matching entity type

### Field Names
- Use snake_case for all fields: `organization_id`, `created_at`
- Boolean fields start with `is_` or `has_`: `is_active`, `has_battery`
- Timestamps end with `_at`: `created_at`, `updated_at`
- IDs end with `_id`: `site_id`, `asset_id`

### ID Format
All identifiers follow a consistent prefixed pattern:

```
{prefix}_{unique_identifier}
```

Standard prefixes:
- `org_` - Organization
- `sit_` - Site
- `ast_` - Asset
- `met_` - Meter
- `sen_` - Sensor
- `tse_` - TimeSeries
- `evt_` - Event
- `usr_` - User
- `api_` - API Key

Example: `ast_solar_panel_42a5`

## Data Types

### Timestamps
- **Always UTC**: No timezone offsets in stored data
- **ISO 8601 Format**: `2025-01-15T14:30:00Z`
- **Precision**: Milliseconds when needed: `2025-01-15T14:30:00.123Z`
- **Field Names**: `created_at`, `updated_at`, `deleted_at`

### Geographic Coordinates
```json
{
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "altitude": 15.5,
    "timezone": "America/Los_Angeles"
  }
}
```
- Decimal degrees (WGS84)
- Altitude in meters above sea level
- Timezone as IANA timezone identifier

### Units of Measurement

All measurements use SI base units unless industry standard differs:

| Measurement | Unit | Symbol | Notes |
|------------|------|--------|-------|
| Power | Watt | W | kilowatt (kW), megawatt (MW) |
| Energy | Watt-hour | Wh | kilowatt-hour (kWh), megawatt-hour (MWh) |
| Voltage | Volt | V | kilovolt (kV) |
| Current | Ampere | A | |
| Frequency | Hertz | Hz | |
| Temperature | Celsius | °C | Kelvin for scientific |
| Pressure | Pascal | Pa | kilopascal (kPa) |
| Irradiance | W/m² | W/m² | Solar radiation |
| Wind Speed | m/s | m/s | meters per second |
| Distance | Meter | m | |
| Mass | Kilogram | kg | |
| Time | Second | s | |

### Enumerations

Define as const arrays with descriptions:

```json
{
  "asset_type": {
    "type": "string",
    "enum": [
      "solar_pv",
      "wind_turbine",
      "battery_storage",
      "diesel_generator",
      "grid_connection"
    ],
    "description": "Type of energy asset"
  }
}
```

### Status Fields

Standard status values across schemas:

```json
{
  "status": {
    "type": "string",
    "enum": ["active", "inactive", "maintenance", "fault", "unknown"],
    "description": "Operational status"
  }
}
```

## Schema Structure

### Required Metadata

Every schema must include:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.qubit.energy/v0.1/asset.json",
  "title": "Asset",
  "description": "Physical energy equipment or device",
  "type": "object"
}
```

### Common Fields

All entity schemas should include:

```json
{
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^ast_[a-zA-Z0-9_-]+$",
      "description": "Unique identifier"
    },
    "name": {
      "type": "string",
      "description": "Human-readable name"
    },
    "description": {
      "type": "string",
      "description": "Detailed description"
    },
    "metadata": {
      "type": "object",
      "description": "Custom fields for extensibility"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Creation timestamp (UTC)"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "Last update timestamp (UTC)"
    }
  }
}
```

### References Between Schemas

Use consistent `*_id` pattern:

```json
{
  "site_id": {
    "type": "string",
    "pattern": "^sit_[a-zA-Z0-9_-]+$",
    "description": "Reference to parent site"
  }
}
```

### Validation Rules

1. **Required Fields**: Minimize to essential only
2. **Patterns**: Use regex for ID validation
3. **Ranges**: Define min/max for numeric fields
4. **String Lengths**: Set reasonable limits
5. **Additional Properties**: Default to `false` except in `metadata`

## Versioning Strategy

### Version Numbers

- **v0.x**: Development, breaking changes allowed
- **v1.0**: First stable release
- **v1.x**: Backward compatible additions
- **v2.0**: Breaking changes

### Backward Compatibility Rules

For minor versions (v1.0 → v1.1):
- ✅ Add optional fields
- ✅ Add new schemas
- ✅ Expand enums
- ❌ Remove fields
- ❌ Change field types
- ❌ Rename fields
- ❌ Make optional fields required

### Migration Path

When breaking changes needed:
1. Deprecate in minor version with warning
2. Provide migration script
3. Document changes clearly
4. Major version bump

## Documentation Standards

### Field Descriptions

Every field must have a description:

```json
{
  "capacity_kwh": {
    "type": "number",
    "minimum": 0,
    "description": "Total energy storage capacity in kilowatt-hours"
  }
}
```

### Examples

Include realistic examples:

```json
{
  "examples": [
    {
      "id": "ast_battery_001",
      "name": "Main Battery Bank",
      "capacity_kwh": 500,
      "power_kw": 100
    }
  ]
}
```

### Schema Documentation

Each schema file should have:
- Clear title and description
- Purpose and use cases
- Relationships to other schemas
- Example JSON in `examples/` directory

## Testing Requirements

1. **Valid Examples**: One valid JSON per schema
2. **Invalid Examples**: Test validation rules
3. **Cross-Schema**: Test references work
4. **Automation**: CI validates all examples

## Security Considerations

1. **No Secrets**: Never include passwords, keys, tokens
2. **PII Handling**: Mark personal data fields clearly
3. **Access Control**: Document but don't implement in schema
4. **Audit Fields**: Include who/when for changes

## Performance Guidelines

1. **Flat Structure**: Avoid deep nesting (max 3 levels)
2. **Array Limits**: Define maxItems where appropriate
3. **String Lengths**: Set reasonable maxLength
4. **Indexable**: Design ID fields for database indexing

## Industry Alignment

Maintain compatibility with:
- **IEC 61850**: Power system communication
- **OCPP 2.0.1**: EV charging protocols
- **OpenADR**: Demand response standards
- **CIM**: Common Information Model

## Extensibility Pattern

Use `metadata` object for custom fields:

```json
{
  "metadata": {
    "type": "object",
    "additionalProperties": true,
    "description": "Custom fields for specific implementations"
  }
}
```

This allows extending without schema changes.

## Review Checklist

Before submitting a schema:
- [ ] Follows naming conventions
- [ ] Includes all required metadata
- [ ] Has descriptions for all fields
- [ ] Uses correct units
- [ ] Validates example data
- [ ] Documents relationships
- [ ] Maintains backward compatibility
- [ ] Includes test cases