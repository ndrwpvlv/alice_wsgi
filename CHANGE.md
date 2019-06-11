# Alice_WSGI change log

## Version 0.0.5
- Added Section class to alice.py for organize large app with modular system. Alice class is parent class for Section
- Updated initial variables for Alice class
```
app = Alice(config, static_path: str = None, templates_path: str = None)
```
Algorithm of setup static and templates path:
```
static_path or self.config.STATIC_PATH_ or '{}/static/'.format(os.getcwd())
templates_path or self.config.TEMPLATES_PATH or '{}/templates/'.format(os.getcwd())
```
- To Router class was added method add_section(section) for registering created with Section class modules.
```
section = Section('/section', Config: object, static_path_of_section: str, templates_path_of_section: str)
```