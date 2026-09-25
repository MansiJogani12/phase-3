import re
import os

path = r"d:\GITHUB\gitforme\gitforme\src\components\Chatbot.jsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update fetch URL
content = content.replace(
    'const response = await fetch("http://localhost:5001/api/chat", {',
    'const apiServerUrl = import.meta.env.VITE_API_URL || "http://localhost:3000";\n      const response = await fetch(`${apiServerUrl}/api/github/${username}/${reponame}/chat`, {'
)

# Add credentials: omit
content = content.replace(
    'body: JSON.stringify(requestBody),\n      });',
    'body: JSON.stringify(requestBody),\n        credentials: "omit",\n      });'
)

# 2. Remove azure logic from handleSendMessage
content = re.sub(
    r'// o\..*?\}', 
    'const headers = { "Content-Type": "application/json" };', 
    content, flags=re.DOTALL
)
# Note: The above didn't work last time because of unicode chars. Let's use a cleaner replacement.
content = re.sub(
    r'const headers = \{ "Content-Type": "application/json" \};\s*if \(azureEndpoint && apiKey && deployment\) \{.*?\n\s*\}',
    'const headers = { "Content-Type": "application/json" };',
    content, flags=re.DOTALL
)

# 3. Remove azure UI from useChat returns
content = re.sub(
    r'azureEndpoint,\s*setAzureEndpoint,\s*apiKey,\s*setApiKey,\s*deployment,\s*setDeployment,\s*apiVersion,\s*setApiVersion,',
    '',
    content
)

# 4. Remove azure UI states from useChat
content = re.sub(
    r'// dY"` Azure Credentials.*?;',
    '',
    content, flags=re.DOTALL
)

# 5. Remove ChatInput props
content = re.sub(
    r'azureEndpoint,\s*setAzureEndpoint,\s*apiKey,\s*setApiKey,\s*deployment,\s*setDeployment,\s*apiVersion,\s*setApiVersion,',
    '',
    content
)

# 6. Remove ChatInput azure UI
content = re.sub(
    r'\{\/\*  Credential Inputs \*\/\}.*?\{\/\* Chat Box \*\/\}',
    '{/* Chat Box */}',
    content, flags=re.DOTALL
)

# 7. Remove warnings
content = re.sub(
    r'disabled=\{showWarning\}',
    '',
    content
)
content = re.sub(
    r'!showWarning && ',
    '',
    content
)
content = re.sub(
    r'\|\| showWarning',
    '',
    content
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
