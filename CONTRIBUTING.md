# Contributing to metric-framework

Thanks for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Run the linting rules against the project itself: `python linting/check_layer_direction.py .`
5. Commit your changes (`git commit -m 'Add my feature'`)
6. Push to the branch (`git push origin feature/my-feature`)
7. Open a Pull Request

## Adding a New KPI Definition

1. Copy `kpi_definitions/examples/ces.yml` as a template
2. Fill in all fields per `kpi_definitions/kpi_schema.yml`
3. Run `python scripts/generate_dictionary.py kpi_definitions/` to verify output

## Adding a New Linting Rule

1. Create a new Python file in `linting/`
2. Follow the pattern: function returns list of error strings, `sys.exit(1)` if errors
3. Add documentation to the README

## Code Style

- Python: follow PEP 8
- SQL: lowercase keywords, 4-space indentation
