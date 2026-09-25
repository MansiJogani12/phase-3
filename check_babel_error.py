import subprocess

try:
    result = subprocess.run(
        'npx babel src/components/RepoDetailView.jsx --presets=@babel/preset-react',
        capture_output=True,
        text=True,
        shell=True,
        cwd=r'd:\GITHUB\gitforme\gitforme'
    )
    print("STDOUT:", result.stdout[:500])
    print("STDERR:", result.stderr[:2000])
except Exception as e:
    print("Error:", e)
