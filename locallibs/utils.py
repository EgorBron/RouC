import typing, jinja2

# import any module from list by name
def import_any(modules: typing.List[str]):
	for module in modules:
		try: return __import__(module)
		except ModuleNotFoundError as e: raise Exception('Cannot import module because there is not') from e
		except ImportError as e: raise Exception('Cannot import module with errors') from e

class ValuesIsSame(Exception): pass
# check if passed only one value and return it
def value_is_once(arg1: object, arg2: object, exctxt = ""):
	if arg1 is None:
		if arg2 is not None: return arg2
	else:
		if arg2 is None: return arg1
	raise ValuesIsSame(exctxt) from ValueError(f"Passed objects '{arg1}' and '{arg2}' is passed at one time")

# render text from template using Jinja2
def render_text(text, **args):
    tm = jinja2.Template(text)
    return tm.render(**args)

# same as above, but async
async def async_render_text(text, **args):
    return await jinja2.Environment(loader=jinja2.loaders.BaseLoader(), enable_async=True).from_string(text).render_async(**args)

# check if two discord objects is not same by its id
def not_same(m1, m2) -> bool:
	"""Check if two discord objects is not same by its ids

	Args:
		m1 (typing.Any): First discord (disnake) object to check
		m2 (typing.Any): Second discord (disnake) object to check

	Returns:
		bool: Check result
	"""
	return not (m1.id == m2.id)