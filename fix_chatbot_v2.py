"""
Targeted rewrite of the useChat hook in Chatbot.jsx:
- Add conversationId state
- Remove dead Azure credential state
- Update request body to send conversation_id
- Parse conversation_id from stream response
- Handle [DONE] sentinel
"""
import re

with open(r'd:\GITHUB\gitforme\gitforme\src\components\Chatbot.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove dead Azure state block
content = re.sub(
    r'  // [^\n]*Azure[^\n]*\n'
    r'  const \[azureEndpoint[^\n]+\n'
    r'  const \[apiKey[^\n]+\n'
    r'  const \[deployment[^\n]+\n'
    r'  const \[apiVersion[^\n]+\n\n'
    r'  const \[showApiKey[^\n]+\n\n',
    '  // Conversation persistence\n  const [conversationId, setConversationId] = useState(null);\n\n',
    content
)

# 2. Remove old "Thinking..." status and replace with context status
content = content.replace(
    'setStatus("Thinking...");',
    'setStatus("Fetching repository context...");'
)

# 3. Update requestBody to include conversation_id
content = re.sub(
    r'const requestBody = \{[^}]+\};',
    'const requestBody = {\n        query: messageText,\n        conversation_id: conversationId,\n      };',
    content,
    count=1
)

# 4. Remove the comment about Azure creds
content = content.replace(
    '      // \U0001f511 Only include Azure creds if all 3 are present\n',
    ''
)
content = content.replace(
    '      // \ufffd\x6f. Only include Azure creds if all 3 are present\n',
    ''
)
# Catch variants
content = re.sub(r'      // [^\n]*Azure creds[^\n]*\n', '', content)

# 5. Update the SSE parser to handle [DONE] and conversation_id
old_parser = '''            try {
              const json = JSON.parse(line.slice(6));
              if (json.token) {'''

new_parser = '''            const raw = line.slice(6).trim();
            if (raw === "[DONE]") return;
            try {
              const json = JSON.parse(raw);
              if (json.conversation_id) {
                setConversationId(json.conversation_id);
              }
              if (json.token) {'''

content = content.replace(old_parser, new_parser, 1)

with open(r'd:\GITHUB\gitforme\gitforme\src\components\Chatbot.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Chatbot.jsx updated.")

# Verify key changes
with open(r'd:\GITHUB\gitforme\gitforme\src\components\Chatbot.jsx', 'r', encoding='utf-8') as f:
    final = f.read()

checks = [
    ("conversationId state", "const [conversationId, setConversationId]" in final),
    ("conversation_id in requestBody", "conversation_id: conversationId" in final),
    ("[DONE] handler", 'raw === "[DONE]"' in final),
    ("setConversationId from stream", "setConversationId(json.conversation_id)" in final),
    ("Azure state removed", "azureEndpoint" not in final),
]

for name, ok in checks:
    print(f"  {'✅' if ok else '❌'} {name}")
