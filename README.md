### Hexlet tests and linter status:
[![Actions Status](https://github.com/RustSaf/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/RustSaf/python-project-52/actions)

### Overview and Installation

"Task Manager" - system similar to http://www.redmine.org/. It allows you to set tasks, assign performers and change their statuses. Login and authentication are required to work with the system.

To deploy the project on the service, you need to specify build and launch commands, as well as set environment variables for working with the PosgresSQL database::

```python

$ make build
$ make render-start

```

The "Task Manager" project is deployed on the service for hosting static websites https://render.com at:
https://python-project-52-y53r.onrender.com


### Links

_This project was built using these tools_:

| Tool                                                                   | Description                                                    |
|------------------------------------------------------------------------|----------------------------------------------------------------|
| [uv](https://docs.astral.sh/uv/)                                       | "An extremely fast Python package and project manager, written |
|                                                                        |  in Rust"                                                      |
| [ruff](https://docs.astral.sh/ruff/)                                   | "An extremely fast Python linter and code formatter, written   |
|                                                                        |  in Rust"                                                      |
| [django](https://www.djangoproject.com/)                               | "Django makes it easier to build better web apps more quickly  |
|                                                                        |  and with less code"                                           |
| [Bootstrap](https://getbootstrap.com/)                                 | "Powerful, extensible, and feature-packed frontend toolkit"    |
| [PostgreSQL](https://www.postgresql.org/)                              | "PostgreSQL is a powerful, open source object-relational       |
|                                                                        |  database system"                                              |
---