import sys

with open('gitforme/src/components/RepoDetailView.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if '<FileHistoryPanel file={selectedFileForHistory}' in line:
        continue
    new_lines.append(line)

lines = new_lines

start_idx = -1
for i, line in enumerate(lines):
    if 'className="flex-grow overflow-y-auto p-0 h-[800px] bg-white flex flex-col"' in line:
        start_idx = i
        break

if start_idx != -1:
    lines[start_idx] = '                        <div className="flex-grow overflow-hidden p-0 h-[800px] bg-white flex">\n                            <div className={`h-full overflow-y-auto transition-all duration-300 flex-grow flex flex-col ${selectedFileForHistory ? "border-r-2 border-black w-2/3" : "w-full"}`}>\n'
    
    div_count = 1
    end_idx = -1
    for i in range(start_idx + 1, len(lines)):
        div_count += lines[i].count('<div')
        div_count -= lines[i].count('</div')
        if div_count <= 0:
            end_idx = i
            break
            
    if end_idx != -1:
        lines[end_idx] = '                            </div>\n' + \
                         '                            {selectedFileForHistory && (\n' + \
                         '                                <div className="w-1/3 flex-shrink-0 h-full overflow-hidden bg-white -ml-[2px] border-l-2 border-black">\n' + \
                         '                                    <FileHistoryPanel file={selectedFileForHistory} history={commitHistory} isLoading={isHistoryLoading} onClose={() => setSelectedFileForHistory(null)} />\n' + \
                         '                                </div>\n' + \
                         '                            )}\n' + \
                         lines[end_idx]

with open('gitforme/src/components/RepoDetailView.jsx', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Updated RepoDetailView.jsx')
