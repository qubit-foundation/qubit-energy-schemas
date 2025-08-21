#!/usr/bin/env python3
"""
Schema validation script for Qubit Energy Schemas.

Validates JSON data files against their corresponding schemas.
Can validate individual files or all examples in the examples directory.
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse
from jsonschema import validate, ValidationError, RefResolver, Draft202012Validator
from jsonschema.exceptions import SchemaError
from tabulate import tabulate
from colorama import init, Fore, Style

init(autoreset=True)


class SchemaValidator:
    """Validates JSON data against Qubit Energy schemas."""
    
    def __init__(self, schema_dir: Path, verbose: bool = False):
        """
        Initialize the validator.
        
        Args:
            schema_dir: Directory containing schema files
            verbose: Enable verbose output
        """
        self.schema_dir = schema_dir
        self.verbose = verbose
        self.schemas: Dict[str, dict] = {}
        self.base_uri = "https://schemas.qubit.energy/v0.1/"
        
    def load_schemas(self) -> None:
        """Load all schemas from the schema directory."""
        schema_files = list(self.schema_dir.glob("*.json"))
        
        if not schema_files:
            raise FileNotFoundError(f"No schema files found in {self.schema_dir}")
        
        for schema_file in schema_files:
            try:
                with open(schema_file, 'r') as f:
                    schema = json.load(f)
                    schema_name = schema_file.stem
                    self.schemas[schema_name] = schema
                    
                    if self.verbose:
                        print(f"  Loaded schema: {schema_name}")
                        
            except json.JSONDecodeError as e:
                print(f"{Fore.RED}✗ Error loading schema {schema_file}: {e}")
                sys.exit(1)
                
    def get_schema_for_file(self, file_path: Path) -> Optional[dict]:
        """
        Get the appropriate schema for a data file.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            The schema dict or None if not found
        """
        # Try to match based on filename
        file_stem = file_path.stem
        
        # Direct match
        if file_stem in self.schemas:
            return self.schemas[file_stem]
        
        # Try singular/plural variations
        if file_stem.endswith('s'):
            singular = file_stem[:-1]
            if singular in self.schemas:
                return self.schemas[singular]
        else:
            plural = file_stem + 's'
            if plural in self.schemas:
                return self.schemas[plural]
        
        return None
    
    def create_resolver(self) -> RefResolver:
        """Create a RefResolver for handling $ref in schemas."""
        # Create a store of all schemas for reference resolution
        store = {}
        for name, schema in self.schemas.items():
            if '$id' in schema:
                store[schema['$id']] = schema
            # Also store by local reference
            store[f"{self.base_uri}{name}.json"] = schema
            
        # Use _definitions as the base if it exists
        if '_definitions' in self.schemas:
            resolver = RefResolver(
                base_uri=self.base_uri,
                referrer=self.schemas['_definitions'],
                store=store
            )
        else:
            # Use first schema as base
            first_schema = next(iter(self.schemas.values()))
            resolver = RefResolver(
                base_uri=self.base_uri,
                referrer=first_schema,
                store=store
            )
            
        return resolver
    
    def validate_file(self, file_path: Path) -> Tuple[bool, str]:
        """
        Validate a JSON file against its schema.
        
        Args:
            file_path: Path to the JSON file to validate
            
        Returns:
            Tuple of (success, message)
        """
        # Load the data file
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {e}"
        except FileNotFoundError:
            return False, f"File not found: {file_path}"
        
        # Get the appropriate schema
        schema = self.get_schema_for_file(file_path)
        if not schema:
            return False, f"No matching schema found for {file_path.name}"
        
        # Create resolver for $ref resolution
        resolver = self.create_resolver()
        
        # Validate
        try:
            validator = Draft202012Validator(schema, resolver=resolver)
            validator.validate(data)
            return True, "Valid"
        except ValidationError as e:
            error_path = " -> ".join(str(p) for p in e.path) if e.path else "root"
            return False, f"Validation error at {error_path}: {e.message}"
        except SchemaError as e:
            return False, f"Schema error: {e.message}"
    
    def validate_directory(self, dir_path: Path) -> List[Tuple[str, bool, str]]:
        """
        Validate all JSON files in a directory.
        
        Args:
            dir_path: Directory containing JSON files
            
        Returns:
            List of (filename, success, message) tuples
        """
        results = []
        json_files = sorted(dir_path.glob("*.json"))
        
        if not json_files:
            print(f"{Fore.YELLOW}No JSON files found in {dir_path}")
            return results
        
        for file_path in json_files:
            success, message = self.validate_file(file_path)
            results.append((file_path.name, success, message))
            
        return results


def print_results(results: List[Tuple[str, bool, str]], verbose: bool = False) -> int:
    """
    Print validation results in a formatted table.
    
    Args:
        results: List of validation results
        verbose: Show detailed error messages
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    if not results:
        print(f"{Fore.YELLOW}No files validated")
        return 0
    
    # Prepare table data
    table_data = []
    failed_count = 0
    
    for filename, success, message in results:
        status = f"{Fore.GREEN}✓ Valid" if success else f"{Fore.RED}✗ Invalid"
        
        if verbose or not success:
            display_message = message[:80] + "..." if len(message) > 80 else message
        else:
            display_message = ""
            
        table_data.append([filename, status, display_message])
        
        if not success:
            failed_count += 1
    
    # Print table
    headers = ["File", "Status", "Details"] if verbose else ["File", "Status", ""]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Print summary
    total = len(results)
    passed = total - failed_count
    
    print(f"\n{Style.BRIGHT}Summary:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Passed: {passed}/{total}")
    if failed_count > 0:
        print(f"  {Fore.RED}Failed: {failed_count}/{total}")
    
    # Print detailed errors for failures
    if failed_count > 0 and not verbose:
        print(f"\n{Fore.YELLOW}Run with --verbose for detailed error messages")
    
    return 0 if failed_count == 0 else 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate JSON files against Qubit Energy schemas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Validate all examples
  %(prog)s examples/site.json        # Validate specific file
  %(prog)s examples/ --verbose       # Validate with detailed output
  %(prog)s --schema-dir custom/path  # Use custom schema directory
        """
    )
    
    parser.add_argument(
        'target',
        nargs='?',
        default='examples',
        help='File or directory to validate (default: examples/)'
    )
    
    parser.add_argument(
        '--schema-dir',
        default='schemas/v0.1',
        help='Directory containing schema files (default: schemas/v0.1)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Exit on first validation error'
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    script_dir = Path(__file__).parent.parent
    schema_dir = script_dir / args.schema_dir
    target_path = script_dir / args.target
    
    # Check schema directory exists
    if not schema_dir.exists():
        print(f"{Fore.RED}✗ Schema directory not found: {schema_dir}")
        sys.exit(1)
    
    # Initialize validator
    print(f"{Style.BRIGHT}Qubit Energy Schema Validator{Style.RESET_ALL}")
    print(f"Schema directory: {schema_dir}")
    
    validator = SchemaValidator(schema_dir, verbose=args.verbose)
    
    # Load schemas
    print(f"\n{Style.BRIGHT}Loading schemas...{Style.RESET_ALL}")
    validator.load_schemas()
    print(f"  Loaded {len(validator.schemas)} schemas")
    
    # Validate target
    print(f"\n{Style.BRIGHT}Validating...{Style.RESET_ALL}")
    
    if target_path.is_file():
        # Validate single file
        success, message = validator.validate_file(target_path)
        results = [(target_path.name, success, message)]
        
    elif target_path.is_dir():
        # Validate directory
        results = validator.validate_directory(target_path)
        
    else:
        print(f"{Fore.RED}✗ Target not found: {target_path}")
        sys.exit(1)
    
    # Print results and exit
    exit_code = print_results(results, verbose=args.verbose)
    
    if exit_code == 0:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ All validations passed!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}{Style.BRIGHT}✗ Validation failed!{Style.RESET_ALL}")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()