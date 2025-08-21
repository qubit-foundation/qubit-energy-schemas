# Qubit Energy Schemas

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Schema Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)](https://github.com/qubit-foundation/qubit-energy-schemas/releases)
[![Validation](https://github.com/qubit-foundation/qubit-energy-schemas/actions/workflows/validate.yml/badge.svg)](https://github.com/qubit-foundation/qubit-energy-schemas/actions/workflows/validate.yml)

Open-source JSON Schema definitions for energy data interchange. Built by the energy community, for the energy community.

## 🎯 Vision

Creating a universal, open standard for energy data that enables seamless integration between energy assets, monitoring systems, and optimization platforms. Our schemas provide a common language for the energy transition.

## ⚡ Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Validate Example Data

```bash
python scripts/validate.py examples/site.json
```

### Use in Your Project

```python
import json
from jsonschema import validate

# Load schema
with open('schemas/v0.1/site.json') as f:
    schema = json.load(f)

# Your data
site_data = {
    "id": "sit_solar_farm_001",
    "name": "North Solar Farm",
    "organization_id": "org_acme_energy",
    "location": {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "timezone": "America/Los_Angeles"
    }
}

# Validate
validate(instance=site_data, schema=schema)
```

## 📊 Core Schemas

| Schema | Description | Example |
|--------|-------------|---------|
| [Organization](schemas/v0.1/organization.json) | Energy company or entity | `examples/organization.json` |
| [Site](schemas/v0.1/site.json) | Physical location with energy assets | `examples/site.json` |
| [Asset](schemas/v0.1/asset.json) | Physical equipment (solar, battery, etc.) | `examples/asset.json` |
| [Meter](schemas/v0.1/meter.json) | Energy measurement device | `examples/meter.json` |
| [Sensor](schemas/v0.1/sensor.json) | Environmental or operational sensor | `examples/sensor.json` |
| [TimeSeries](schemas/v0.1/timeseries.json) | Time-stamped measurements | `examples/timeseries.json` |

## 🔧 Key Features

- **Standardized IDs**: Consistent prefixed identifiers (`org_`, `sit_`, `ast_`, etc.)
- **UTC Timestamps**: All times in ISO 8601 UTC format
- **SI Units**: Standardized on International System of Units
- **Extensible**: Support for custom fields via `metadata` objects
- **Versioned**: Clear versioning strategy for backward compatibility
- **Validated**: Automated validation with comprehensive test coverage

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-schema`)
3. Make your changes
4. Run validation (`python scripts/validate.py`)
5. Submit a Pull Request

## 🗺️ Roadmap

- **v0.1** (Current): Core schemas for basic energy infrastructure
- **v0.2**: Grid interconnection and power quality schemas
- **v0.3**: Market signals, tariffs, and demand response
- **v0.4**: Forecasting and optimization schemas
- **v1.0**: Production-ready with full test coverage

## 🔗 Standards Compatibility

Our schemas are designed to interoperate with:
- IEC 61850 (Power Systems)
- OCPP 2.0.1 (EV Charging)
- OpenADR 2.0 (Demand Response)
- IEEE 2030.5 (Smart Energy)

See [docs/standards-mapping.md](docs/standards-mapping.md) for detailed mappings.

## 📚 Documentation

- [Schema Conventions](docs/schema-conventions.md) - Design principles and guidelines
- [Standards Mapping](docs/standards-mapping.md) - Interoperability with industry standards
- [Examples](examples/) - Sample data for each schema
- [API Integration](docs/api-integration.md) - Using schemas in REST/GraphQL APIs

## 💬 Community

- **Discussions**: [GitHub Discussions](https://github.com/qubit-foundation/qubit-energy-schemas/discussions)
- **Issues**: [GitHub Issues](https://github.com/qubit-foundation/qubit-energy-schemas/issues)
- **Discord**: [Join our Discord](https://discord.gg/energy-schemas)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with contributions from energy professionals, software engineers, and sustainability advocates worldwide.

---

**Building the data foundation for the energy transition.** 🌍⚡