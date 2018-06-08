# TSP with Greedy and 2-Opt

## Compile and run against any input file
`make tsp && ./tsp path/to/testFile`

Output will generate in tests/mytest.txt.tour

## TSP-Verifier
To verify that all locations were added to the solution file
`python tsp-verifier.py [input filepath] [solution filepath]`

## Timing
To verify that all algorithms run in the required 3 minute time
`python watch.py python tsp.py [input filepath]`
