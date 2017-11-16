deploy:
	cp -f src/* ~/.task/hooks

clean:
	find . -name "*.pyc" -exec rm -f {} \;

test:
	py.test tests --fulltrace -vv

quicktest:
	py.test tests -vv
