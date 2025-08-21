#!/usr/bin/env python3
"""
Generate TypeScript type definitions from JSON schemas.

This script converts Qubit Energy JSON schemas to TypeScript interfaces,
making it easy to use the schemas in TypeScript/JavaScript projects.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import argparse
import re
from datetime import datetime


class TypeScriptGenerator:
    """Generates TypeScript types from JSON schemas."""
    
    def __init__(self, schema_dir: Path, output_dir: Path):
        """
        Initialize the generator.
        
        Args:
            schema_dir: Directory containing schema files
            output_dir: Directory for generated TypeScript files
        """
        self.schema_dir = schema_dir
        self.output_dir = output_dir
        self.schemas: Dict[str, dict] = {}
        self.generated_types: set = set()
        
    def load_schemas(self) -> None:
        """Load all schemas from the schema directory."""
        schema_files = list(self.schema_dir.glob("*.json"))
        
        for schema_file in schema_files:
            with open(schema_file, 'r') as f:
                schema = json.load(f)
                schema_name = schema_file.stem
                self.schemas[schema_name] = schema
                
    def json_type_to_typescript(self, json_type: Any, schema: dict = None) -> str:
        """
        Convert JSON schema type to TypeScript type.
        
        Args:
            json_type: JSON schema type definition
            schema: Full schema object for context
            
        Returns:
            TypeScript type string
        """
        if isinstance(json_type, list):
            # Union type
            types = [self.json_type_to_typescript(t, schema) for t in json_type]
            return " | ".join(types)
        
        if json_type == "string":
            if schema:
                if schema.get("format") == "date-time":
                    return "string"  # Could be Date, but string is safer
                elif schema.get("format") == "date":
                    return "string"
                elif schema.get("format") == "email":
                    return "string"
                elif schema.get("format") == "uri":
                    return "string"
                elif schema.get("format") in ["ipv4", "ipv6"]:
                    return "string"
                elif "enum" in schema:
                    # Create union type from enum values
                    values = [f'"{v}"' for v in schema["enum"]]
                    return " | ".join(values)
            return "string"
        elif json_type == "number":
            return "number"
        elif json_type == "integer":
            return "number"
        elif json_type == "boolean":
            return "boolean"
        elif json_type == "null":
            return "null"
        elif json_type == "array":
            if schema and "items" in schema:
                item_type = self.process_property("item", schema["items"])
                return f"{item_type}[]"
            return "any[]"
        elif json_type == "object":
            if schema and "properties" in schema:
                return self.generate_interface_body(schema["properties"], schema.get("required", []))
            return "Record<string, any>"
        else:
            return "any"
    
    def process_property(self, name: str, prop: dict) -> str:
        """
        Process a single property definition.
        
        Args:
            name: Property name
            prop: Property schema
            
        Returns:
            TypeScript type string
        """
        # Handle $ref
        if "$ref" in prop:
            ref_path = prop["$ref"]
            # Extract type name from reference
            if "#/$defs/" in ref_path:
                type_name = ref_path.split("/")[-1]
                return self.pascal_case(type_name)
            elif ".json#" in ref_path:
                # Reference to another schema
                schema_name = ref_path.split("/")[-1].replace(".json", "")
                return self.pascal_case(schema_name)
            else:
                return "any"
        
        # Handle oneOf
        if "oneOf" in prop:
            types = []
            for option in prop["oneOf"]:
                types.append(self.process_property(name, option))
            return " | ".join(types)
        
        # Handle regular types
        if "type" in prop:
            return self.json_type_to_typescript(prop["type"], prop)
        
        return "any"
    
    def pascal_case(self, snake_str: str) -> str:
        """Convert snake_case to PascalCase."""
        components = snake_str.split('_')
        return ''.join(x.title() for x in components)
    
    def generate_interface_body(self, properties: dict, required: List[str]) -> str:
        """
        Generate the body of a TypeScript interface.
        
        Args:
            properties: Schema properties
            required: List of required property names
            
        Returns:
            Interface body string
        """
        lines = ["{"]
        
        for prop_name, prop_schema in properties.items():
            # Determine if property is optional
            optional = "?" if prop_name not in required else ""
            
            # Get TypeScript type
            ts_type = self.process_property(prop_name, prop_schema)
            
            # Add JSDoc comment if description exists
            if "description" in prop_schema:
                lines.append(f"  /** {prop_schema['description']} */")
            
            # Add property definition
            lines.append(f"  {prop_name}{optional}: {ts_type};")
        
        lines.append("}")
        return "\n".join(lines)
    
    def generate_definitions(self) -> str:
        """Generate TypeScript definitions from _definitions schema."""
        if "_definitions" not in self.schemas:
            return ""
        
        output = []
        definitions = self.schemas["_definitions"].get("$defs", {})
        
        for def_name, def_schema in definitions.items():
            interface_name = self.pascal_case(def_name)
            
            if interface_name in self.generated_types:
                continue
            
            self.generated_types.add(interface_name)
            
            # Special handling for different definition types
            if def_name == "id_patterns":
                # Generate type aliases for ID patterns
                for id_type, id_schema in def_schema.items():
                    type_name = self.pascal_case(id_type)
                    output.append(f"/** {id_schema.get('description', '')} */")
                    output.append(f"export type {type_name} = string;")
                    output.append("")
            elif "properties" in def_schema:
                # Generate interface
                output.append(f"/** {def_schema.get('description', '')} */")
                output.append(f"export interface {interface_name} {{")
                
                required = def_schema.get("required", [])
                for prop_name, prop_schema in def_schema["properties"].items():
                    optional = "?" if prop_name not in required else ""
                    ts_type = self.process_property(prop_name, prop_schema)
                    
                    if "description" in prop_schema:
                        output.append(f"  /** {prop_schema['description']} */")
                    output.append(f"  {prop_name}{optional}: {ts_type};")
                
                output.append("}")
                output.append("")
            elif "type" in def_schema:
                # Generate type alias
                ts_type = self.json_type_to_typescript(def_schema["type"], def_schema)
                output.append(f"/** {def_schema.get('description', '')} */")
                output.append(f"export type {interface_name} = {ts_type};")
                output.append("")
        
        return "\n".join(output)
    
    def generate_schema_interface(self, schema_name: str, schema: dict) -> str:
        """
        Generate TypeScript interface for a schema.
        
        Args:
            schema_name: Name of the schema
            schema: Schema definition
            
        Returns:
            TypeScript interface string
        """
        interface_name = self.pascal_case(schema_name)
        output = []
        
        # Add header comment
        output.append(f"/**")
        output.append(f" * {schema.get('title', interface_name)}")
        if "description" in schema:
            output.append(f" * {schema['description']}")
        output.append(f" */")
        
        # Generate interface
        output.append(f"export interface {interface_name} {{")
        
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        for prop_name, prop_schema in properties.items():
            optional = "?" if prop_name not in required else ""
            ts_type = self.process_property(prop_name, prop_schema)
            
            # Add description as comment
            if "description" in prop_schema:
                output.append(f"  /** {prop_schema['description']} */")
            
            output.append(f"  {prop_name}{optional}: {ts_type};")
        
        output.append("}")
        
        return "\n".join(output)
    
    def generate_index_file(self) -> str:
        """Generate index.ts file that exports all types."""
        output = []
        output.append("/**")
        output.append(" * Qubit Energy Schemas - TypeScript Type Definitions")
        output.append(f" * Generated on {datetime.now().isoformat()}")
        output.append(" */")
        output.append("")
        
        # Export common definitions
        output.append("// Common definitions and enums")
        output.append("export * from './definitions';")
        output.append("")
        
        # Export each schema
        output.append("// Schema interfaces")
        for schema_name in sorted(self.schemas.keys()):
            if schema_name != "_definitions":
                output.append(f"export * from './{schema_name}';")
        
        return "\n".join(output)
    
    def generate_all(self) -> None:
        """Generate all TypeScript files."""
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate definitions file
        definitions_content = self.generate_definitions()
        if definitions_content:
            definitions_file = self.output_dir / "definitions.ts"
            with open(definitions_file, 'w') as f:
                f.write("// Common definitions and types\n\n")
                f.write(definitions_content)
            print(f"  Generated: {definitions_file.name}")
        
        # Generate interface for each schema
        for schema_name, schema in self.schemas.items():
            if schema_name == "_definitions":
                continue
            
            interface_content = self.generate_schema_interface(schema_name, schema)
            output_file = self.output_dir / f"{schema_name}.ts"
            
            with open(output_file, 'w') as f:
                # Add imports if needed
                f.write("import { ")
                imports = []
                
                # Check for references to definitions
                schema_str = json.dumps(schema)
                if "id_patterns" in schema_str:
                    imports.extend(["OrganizationId", "SiteId", "AssetId", "MeterId", "SensorId", "TimeseriesId"])
                if "_definitions.json" in schema_str:
                    imports.extend(["Location", "Status", "Metadata", "Contact"])
                
                if imports:
                    f.write(", ".join(set(imports)))
                    f.write(" } from './definitions';\n\n")
                else:
                    f.write("} from './definitions';\n\n")
                
                f.write(interface_content)
                f.write("\n")
            
            print(f"  Generated: {output_file.name}")
        
        # Generate index file
        index_file = self.output_dir / "index.ts"
        with open(index_file, 'w') as f:
            f.write(self.generate_index_file())
        print(f"  Generated: {index_file.name}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate TypeScript types from Qubit Energy schemas"
    )
    
    parser.add_argument(
        '--schema-dir',
        default='schemas/v0.1',
        help='Directory containing schema files'
    )
    
    parser.add_argument(
        '--output-dir',
        default='generated/types',
        help='Output directory for TypeScript files'
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    script_dir = Path(__file__).parent.parent
    schema_dir = script_dir / args.schema_dir
    output_dir = script_dir / args.output_dir
    
    # Check schema directory
    if not schema_dir.exists():
        print(f"Error: Schema directory not found: {schema_dir}")
        sys.exit(1)
    
    print("TypeScript Type Generator")
    print(f"Schema directory: {schema_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Generate types
    generator = TypeScriptGenerator(schema_dir, output_dir)
    generator.load_schemas()
    print(f"Loaded {len(generator.schemas)} schemas")
    print()
    
    print("Generating TypeScript types...")
    generator.generate_all()
    
    print()
    print("✓ TypeScript types generated successfully!")
    print(f"  Output: {output_dir}/")
    print()
    print("To use in your TypeScript project:")
    print(f"  import {{ Organization, Site, Asset }} from './{output_dir.name}';")


if __name__ == "__main__":
    main()