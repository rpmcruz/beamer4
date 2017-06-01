import sys
import re

if len(sys.argv) <= 1:
	print("Usage: %s INPUT [OUTPUT]" % sys.argv[0])
	sys.exit(1)

input_filename = sys.argv[1]
if len(sys.argv) > 2:
    output_filename = sys.argv[2]
else:
    output_filename = input_filename[:-4] + '4.tex'

input = open(input_filename,'r')
output = open(output_filename,'w')

special_header = ''
special_frames = []
inside_frame = False

output.write(input.readline())  # header

output.write(r'''
\usepackage[skins]{tcolorbox}
\newtcolorbox{Active}{boxsep=0pt, colback=yellow!50, width=0.5\textwidth, height=0.46\textheight, left=1mm, right=1mm, top=1mm, bottom=1mm, boxrule=0pt, frame hidden, bicolor, sharp corners, nobeforeafter}
\newtcolorbox{TInactive}{boxsep=0pt, colback=white, width=0.5\textwidth, height=0.46\textheight, left=1mm, right=1mm, top=1mm, bottom=1mm, boxrule=0pt, frame hidden, bicolor, sharp corners, nobeforeafter}
\newenvironment{Inactive}{%
\begin{TInactive}%
\setbeamercolor{normal text}{fg=gray}%
\usebeamercolor[fg]{normal text}%
\setbeamercolor{structure}{fg=gray}%
\usebeamercolor[fg]{structure}%
\setbeamercolor{itemize item}{fg=gray}%
\setbeamercolor{itemize subitem}{fg=gray}%
}{%
\end{TInactive}}
''')

# inves de top, bottom, left, right... podes meter fbox, small

for line in input:
    if line.startswith(r'\begin{frame}'):
        if '%frame4' in line:
            inside_frame = True
            special_frames.append('')
            special_header = line
        else:
            special_frames = []
            output.write(line)
    elif inside_frame:
        if line.startswith(r'\end{frame}'):
            output.write(special_header)
            frames = special_frames[-4:]
            len_frames = len(special_frames)
            old_order = range(max(0, len_frames-4), len_frames)
            order = [i % 2 if i % 4 < 2 else 1-(i % 2)+2 for i in old_order]
            frames = sorted(zip(order, frames))
            if len(frames) == 3:
                frames.insert(2, (2, ''))
            for i, frame in frames:
                is_active = frame == special_frames[-1]
                if is_active:
                    output.write(r'\begin{Active}')
                else:
                    output.write(r'\begin{Inactive}')
                output.write(frame)
                if is_active:
                    output.write(r'\end{Active}')
                else:
                    output.write(r'\end{Inactive}')
                if i+1 < len(frames):
                    if i % 2 == 0:
                        output.write(r'\hfill')
                    else:
                        output.write(r'\\')
            output.write('\n')
            output.write(r'\end{frame}')
            output.write('\n')
            inside_frame = False
        else:
            special_frames[-1] += line
    else:
        output.write(line)

input.close()
output.close()
