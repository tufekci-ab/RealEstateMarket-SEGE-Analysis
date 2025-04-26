@echo off
echo [1/4] Running preprocessing...
python src\processBeforeEDA.py

echo [2/4] Running EDA...
python src\EDA-Calculator.py

echo [3/4] Creating PDF report...
python src\PDF-Maker.py

echo [4/4] Running hypothesis test...
python src\hypothesis-tester.py

echo All steps completed successfully.
pause