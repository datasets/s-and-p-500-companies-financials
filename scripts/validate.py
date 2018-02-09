from pprint import pprint
from goodtables import validate

validation_report = validate(
    '../datapackage.json', preset='datapackage')

pprint(validation_report)

if not validation_report['valid'] == True:
    raise RuntimeError('The data did not pass validation.')
