run:
	rm parser.out parsetab.py *.pyc
	./g984parser.py T-REC-G.988-201210-I\!\!PDF-E.txt 2>&1 | less

.PHONY: run
