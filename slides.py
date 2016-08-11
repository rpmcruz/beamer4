#!/usr/bin/env python3

import sys, re, os
HAS_BIBLIOGRAPHY = False

if len(sys.argv) <= 1:
	print("Usage: %s INPUT [OUTPUT]" % sys.argv[0])
	sys.exit(1)

begin = re.compile('^\\\\begin{frame}{(.+)}')
end = re.compile('\\\\end{frame}$')
comment = re.compile('^%%%%%%%')

groups = []
frames = []
within_frame = False
title = ""
text = ""

filename = sys.argv[1]
f = open(filename,'r')
for line in f:
	if comment.search(line):
		groups.append(frames)
		frames = []
	result = begin.search(line)
	if result:
		within_frame = True
		title = result.group(1)
	elif within_frame:
		result = end.search(line)
		if result:
			within_frame = False
			frames.append((title,text))
			text = ""
		else:
			text += line
groups.append(frames)
f.close()

#print(frames)

## Fall back: one per slide

output = 'output'
if len(sys.argv) >= 3:
    output = sys.argv[2].split(".")[0]

o = output + "2"
out = open(o+".tex",'w')

out.write("%% arara: pdflatex\n")
if HAS_BIBLIOGRAPHY:
    out.write("%% arara: biber\n%% arara: pdflatex\n")
out.write("%% arara: pdflatex\n%% arara: clean: { files: [%s.aux,%s.log,%s.nav,%s.out,%s.snm,%s.toc,%s.run.xml,%s.bbl,%s.bcf,%s.blg] }\n\n" % (o,o,o,o,o,o,o,o,o,o))
out.write("\\documentclass{beamer}\n\\usepackage{style}\n\n")

out.write("\\begin{document}\n")
for frames in groups:
	for frame in frames:
		out.write("\\begin{frame}{%s}%s\\end{frame}\n" % (frame[0], frame[1]))
out.write("""\\begin{frame}[allowframebreaks]{References}
""")
if HAS_BIBLIOGRAPHY:
    out.write("\\printbibliography\n")
out.write("""\\end{frame}
""")
out.write("\\end{document}\n")
out.close()
os.system("arara %s >/dev/null &" % (o+".tex"))

## Normal: quadrant mode !

o = output
out = open(o+".tex",'w')

out.write("%% arara: pdflatex\n")
if HAS_BIBLIOGRAPHY:
    out.write("%% arara: biber\n%% arara: pdflatex\n")
out.write("%% arara: pdflatex\n%% arara: clean: { files: [%s.aux,%s.log,%s.nav,%s.out,%s.snm,%s.toc,%s.run.xml,%s.bbl,%s.bcf,%s.blg] }\n\n" % (o,o,o,o,o,o,o,o,o,o))
out.write("\\documentclass[t,9pt]{beamer}\n\\usepackage{style}\n")
out.write("\\setbeamersize{text margin left=0.5em, text margin right=0.5em}\n")
out.write("\n")

for i in range(4):
	out.write("\\newcommand\FourQuad%s[4]{\n" % (chr(i+ord('A'))))
	for j in range(4):
		k = j if j<=1 else (3-j)+2
		out.write("\\colorbox{%s}{" % ("yellow!50" if i==k else "white"))
		if i!=k:
			out.write("%%\n\\setbeamercolor{normal text}{fg=gray}\\usebeamercolor[fg]{normal text}%\n")
			out.write("\\setbeamercolor{structure}{fg=gray}\\usebeamercolor[fg]{structure}%%\n")
			out.write("\\setbeamercolor{itemize item}{fg=gray}%%\n")
			out.write("\\setbeamercolor{itemize subitem}{fg=gray}%%\n")
		out.write("\\begin{minipage}[b][.438\\textheight][t]{.4825\\textwidth}#%d\end{minipage}" % (k+1))
		out.write("}")
		if j%2==0: out.write("\\hfill\n")
		else:      out.write("\\\\\n")
	out.write("}\n")

def write_columns(title, t1, t2, t3, t4, i):
	out.write("\\begin{frame}{%s}\\FourQuad%s{\n%s\n}{\n%s\n}{\n%s\n}{\n%s\n}\\end{frame}\n" % (title, chr(i+ord('A')), t1, t2, t3, t4))

out.write("\\begin{document}\n")
for frames in groups:
	if len(frames) == 1:
		figure = frames[0][1].find('\\includegraphics') > 0
		if figure:
			out.write("\\bgroup\\setbeamertemplate{logo}{}\n\\setbeamercolor{background canvas}{bg=gray}\n")
		out.write("\\begin{frame}[c]{%s}\n%s\n\\end{frame}\n" % (frames[0][0], frames[0][1]))
		if figure:
			out.write("\\egroup\n")
	else:
		slides = [0,0,0,0]
		for i in range(len(frames)):
			slides[i%4] = i
			write_columns(
				frames[i][0],
				frames[slides[0]][1],
				"" if slides[1]==0 else frames[slides[1]][1],
				"" if slides[2]==0 else frames[slides[2]][1],
				"" if slides[3]==0 else frames[slides[3]][1],
				i%4)
if HAS_BIBLIOGRAPHY:
    out.write("""\\begin{frame}{References}
\\begin{multicols}{2}
{\\footnotesize\\printbibliography}
\\end{multicols}
\\end{frame}
""")

out.write("\\end{document}\n")
out.close()
os.system("arara -v %s" % (output+".tex"))
#os.remove(output+".tex")
#os.remove(output+"2.tex")

