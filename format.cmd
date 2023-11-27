autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
isort --apply app
ruff format app