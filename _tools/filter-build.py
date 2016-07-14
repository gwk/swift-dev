#!/usr/bin/env python3

import re
from sys import stdin, argv
from pithy.ansi import ERASE_LINE, TXT_L, TXT_C, TXT_Y, RST_TXT 

args = argv[1:]

cr = '\n' if ('-dbg' in args) else '\r'

r = re.compile(r'''(?x)
  ^\+
| ~/
| --$
| --\s+[A-Z]
| ---\ bootstrap:\ note:
| .+:\ using\ standard\ linker$
| \s+export
| \s+cd

| \[\d+/\d+\]$
| \[\d+/\d+\]\ (?:Building|Generating|Install|Linking|Symlinking)
| \[\d+/\d+\]\ (?:AR|CXX|INLINE|LINK|RE2C)
| \[\d+/\d+\]\ .+/cmake\ -E
| \[\d+/\d+\]\ cd
| \[\d+/\d+\]\ (?:Building|Copying)
| (\[\d+/\d+\]\ )? .+/((?:clang|clang\+\+|cmake|dsymutil|libtool|mig|swift|swiftc|touch)'?)\ (?:.* (-[oc]\ \S+))+

| .+/(swiftc) .* (-module-name\ \S+ | --driver-mode=swift)

| .*builtin-(?:copy|infoPlistUtility|swiftStdLibTool) \s
| .*(?:cd|chmod|ditto|echo|ld|make|strip|write-file) \s
| \s*/bin/(?:chmod|ln|mkdir|sh) \s
| \s*/usr/sbin/chown \s
| (CompileC) .+? (\S+\.(?:c|cpp|m|mm))
| (CompileSwift) .+? (\S+\.swift)
| (?:CopySwiftLibs|CpHeader|CpResource|Ditto|ExternalBuildToolExecution|GenerateDSYMFile|Ld|Libtool|MergeSwiftModule|Mig|PBXCp|PhaseScriptExecution|ProcessInfoPlistFile|SetOwnerAndGroup|SetMode|Strip|SymLink|Touch)

| ld:\ warning:
| .+/bin/(libtool: .*)
| .+/bin/(ranlib:) .* (for\ architecture:\ \w+)? .* (file:\ [^\s]+) .* (has\ no\ symbols)

# sphinx
| building\ .+:
| checking\ consistency
| copying\ extra\ files
| copying\ images
| copying\ static\ files
| dumping\ object\ inventory
| dumping\ search\ index
| generating\ indices
| loading\ pickled\ environment
| looking\ for\ now-outdated\ files
| making\ output\ directory
| pickling\ environment
| preparing\ documents
| reading\ sources
| updating\ environment:
| writing\ additional\ pages
| writing\ output

| Check\ dependencies
| Create\ product\ structure
| Write\ auxiliary\ files

| Copying\ .+\ from\ .+\ to\ .*
| Build\ settings\ from\ command\ line:$
| \s+[A-Z_]+\ =

| .+ \.gyb: .+ warning:\ default\ will\ never\ be\ executed
| [ ~^]+$
| .+ ExpressibleBy # TEMPORARY
| (?: extension | public\ class| public\ struct ) # TEMPORARY
| \s+default:$ # TEMPORARY?
''')

def line_num(index): return '{:05}'.format(index)

omit_start = None
omit_last = None
def clear():
  global omit_start
  global omit_last
  if omit_start is not None:
    if omit_start < omit_last:
      last = '-{} omitted ({})'.format(line_num(omit_last), 1 + omit_last - omit_start)
    else:
      last = ' omitted'
    print(TXT_Y, line_num(omit_start), last, RST_TXT, sep='')
  omit_start = None
  omit_last = None

for index, raw_line in enumerate(stdin, 1):
  if raw_line.isspace(): continue
  line = raw_line.rstrip()
  num = line_num(index)
  m = r.match(line)
  if m:
    if omit_start is None:
      omit_start = index
    omit_last = index
    g = tuple(g for g in m.groups('') if g) 
    msg = ' '.join(g) if g else line
    if len(msg) > 192: msg = msg[:192] + '…'
    print(TXT_C, num, ': ', msg, RST_TXT, sep='', end=cr, flush=True)
    print(ERASE_LINE, end='', flush=False)
  else:
    clear()
    match_index = index + 1
    print(TXT_L, num, ': ', line, RST_TXT, sep='')

clear()
