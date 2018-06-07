# TSP
## To Run
As of right now we only support python 2

run
`python tsp.py path/to/inputs.txt`
to run the TSP module
ex:
`python tsp.py tests/mytest.txt`
from the root directory

output will generate in tests/mytest.txt.tour

## Tests
To run the tests,
run
`python tests.py`

## TSP-Verifier
To verify that all locations were added to the solution file
`python tsp-verifier.py [input filepath] [solution filepath]`

## Timing
To verify that all algorithms run in the required 3 minute time
`python watch.py python tsp.py [input filepath]`
