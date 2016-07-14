# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# $@: The file name of the target of the rule.
# $<: The name of the first prerequisite.
# $^: The names of all the prerequisites, with spaces between them. 

.PHONY: default build clean install test test-long test-validation update

default: build

build:
	_tools/build.sh rel-dbg assert

clean:
	rm -rf _build/*

setup:
	git clone git@github.com:apple/swift.git
	swift/utils/update-checkout --clone-with-ssh

install: toolchain
	SRC=_build/rel-dbg_assertions/install/Library/Developer/Toolchains/swift-local.xctoolchain
	DST=/Library/Developer/Toolchains/
	cp -r  $SRC $DST

test:
	sh/build.sh --test

test-validation:
	sh/build.sh --validation-test

test-long:
	sh/build.sh --long-test

toolchain: build

update:
	swift/utils/update-checkout
