#!/usr/bin/env bash

set -eu
set -o pipefail

error() { echo "build-toolchain.sh error: $@" 1>&2; exit 1; }

cd $(dirname "$0")/..

opt="$1"; shift || error "please specify optimization level: debug | rel-dbg | release."
assert="$1"; shift || error "please specify assertion mode: assert | no-assert."

echo "building for optimization level: $opt"

DATE=$(date +"%Y-%m-%d_%H_%M")

BUILD_ROOT="$PWD/_build"
BUILD_NAME="${opt}_${assert}"
BUILD_DIR="$BUILD_ROOT/$BUILD_NAME"

mkdir -p "$BUILD_DIR"

time \
SWIFT_SOURCE_ROOT="$PWD" \
SWIFT_BUILD_ROOT="$BUILD_ROOT" \
swift/utils/build-script \
--jobs=6 \
--build-subdir="$BUILD_NAME" \
--${opt/rel-dbg/release-debuginfo} \
--${assert}ions \
--foundation \
--llbuild \
--lldb \
--swiftpm \
--xctest \
--skip-build-libdispatch \
--ios \
--tvos \
--watchos \
"$@" \
-- \
--build-ninja \
--build-swift-static-stdlib \
--compiler-vendor=apple \
--darwin-install-extract-symbols \
--darwin-toolchain-alias=Local \
--darwin-toolchain-bundle-identifier=swift_local \
--darwin-toolchain-display-name-short='Swift Local Build' \
--darwin-toolchain-display-name='Swift Local Build - $DATE' \
--darwin-toolchain-name=swift-local \
--darwin-toolchain-version="swift-local_$DATE" \
--install-destdir="$BUILD_DIR/install" \
--install-llbuild \
--install-lldb \
--install-prefix=/Library/Developer/Toolchains/swift-local.xctoolchain/usr \
--install-swift \
--install-swiftpm \
--install-symroot="$BUILD_DIR/symroot" \
--installable-package="$BUILD_DIR/swift-local.tar.gz" \
--lldb-build-type=Release \
--lldb-no-debugserver \
--lldb-use-system-debugserver \
--llvm-install-components='libclang;libclang-headers' \
--reconfigure \
--swift-enable-ast-verifier=0 \
--swift-install-components='compiler;clang-builtin-headers;stdlib;sdk-overlay;license;sourcekit-xpc-service;swift-remote-mirror;swift-remote-mirror-headers' \
--symbols-package="$BUILD_DIR/swift-local-symbols.tar.gz" \
--test-installable-package \
--verbose-build \
2>&1 | tee "$BUILD_DIR/$BUILD_NAME.log" | _tools/filter-build.py


# --libdispatch breaks on LIBTOOL nonsense.

# debug overrides: --debug-{llvm,swift,swift-stdlib,lldb,cmark,foundation,libdispatch)

# --test, --long-test, --validation-test.

# -lto={thin,full}

# --no-swift-stdlib-assertions

#--
#
#--build-swift-stdlib-unittest-extra
