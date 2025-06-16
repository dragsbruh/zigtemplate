sample:
	cd samples && \
	rm -rf zig_project && \
	cookiecutter .. --no-input && \
	cd zig_project && \
	zig build run
