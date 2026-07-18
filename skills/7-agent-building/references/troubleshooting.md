# Troubleshooting Guide - DevRev Agent Building Toolkit

> **Purpose:** Common issues, root causes, and solutions discovered through real-world usage.

---

## Issue #1 — Network Permission Errors (Exit Code 56)

**Symptom:**
```bash
curl command fails with exit code 56
Empty response from API endpoints
```

**Root Cause:**
Sandbox restrictions limit network access to allowed domains only. DevRev API calls require unrestricted network access.

**Solution:**
Always add `required_permissions: ["full_network"]` to Shell commands that call DevRev APIs:

```bash
Shell(
  command="curl -X POST 'https://api.devrev.ai/internal/ai-agents.get' ...",
  required_permissions=["full_network"]
)
```

**Prevention:**
- All scripts in `scripts/` directory should document network requirements
- Add network permission checks to helper functions

---

## Issue #2 — Article Content Extraction: `published_version` is null

**Symptom:**
```json
{
  "article": {
    "title": "My Article",
    "published_version": null
  }
}
```

**Root Cause:**
Not all articles have a `published_version.body` field. Draft articles or articles with attachments store content in `extracted_content` field instead.

**Solution - Multi-Step Content Extraction:**

1. **Try `published_version.body` first** (fastest, for published articles):
```bash
body=$(jq -r '.article.published_version.body // empty' article.json)
```

2. **If null, check `extracted_content[0].original_url`** (for articles with extracted text):
```bash
if [ -z "$body" ]; then
  url=$(jq -r '.article.extracted_content[0].original_url // empty' article.json)
  if [ -n "$url" ]; then
    curl -s "$url" > extracted_content.txt
  fi
fi
```

3. **If still null, check `resource.artifacts[0]`** (for articles with rich text attachments):
```bash
if [ -z "$body" ]; then
  rt_url=$(jq -r '.article.resource.artifacts[0].original_url // empty' article.json)
  # Note: devrev/rt format may require special handling
fi
```

**Helper Function:**
```bash
# Get article content with fallback strategy
get_article_content() {
  local article_id="$1"
  local output_file="$2"
  
  # Fetch article metadata
  local article_json=$(curl -s -X POST 'https://api.devrev.ai/internal/articles.get' \
    -H "Authorization: ${ORG_PAT}" \
    -H 'Content-Type: application/json' \
    -d "{\"id\": \"${article_id}\"}")
  
  # Try published_version.body
  local body=$(echo "$article_json" | jq -r '.article.published_version.body // empty')
  if [ -n "$body" ]; then
    echo "$body" > "$output_file"
    return 0
  fi
  
  # Try extracted_content
  local extracted_url=$(echo "$article_json" | jq -r '.article.extracted_content[0].original_url // empty')
  if [ -n "$extracted_url" ]; then
    curl -s "$extracted_url" > "$output_file"
    return 0
  fi
  
  # Try resource artifacts (devrev/rt format)
  local artifact_url=$(echo "$article_json" | jq -r '.article.resource.artifacts[0].original_url // empty')
  if [ -n "$artifact_url" ]; then
    # Warning: devrev/rt format may not be plain text
    curl -s "$artifact_url" > "$output_file"
    echo "Warning: Article content is in devrev/rt format, may require special parsing" >&2
    return 0
  fi
  
  echo "Error: No content found for article ${article_id}" >&2
  return 1
}
```

---

## Issue #3 — Binary Article Attachments (devrev/rt, .xlsx, .docx)

**Symptom:**
```
Read tool error: "Binary files of type .xlsx are not supported"
Article has content_format: "rt" but content is not plain text
```

**Root Cause:**
Some articles have attachments in binary formats:
- `devrev/rt` — DevRev's internal rich text format
- `.xlsx` — Excel files
- `.docx` — Word documents
- `.pdf` — PDF files

**Solution:**
1. **Check `file.type` before attempting to read**:
```bash
file_type=$(jq -r '.article.extracted_content[0].file.type // .article.resource.artifacts[0].file.type' article.json)

if [[ "$file_type" == "text/plain" ]]; then
  # Safe to download and read as text
  curl -s "$url" > content.txt
elif [[ "$file_type" == "devrev/rt" ]]; then
  echo "Article is in DevRev rich text format - may not be plain text"
  # Attempt download, but content may not be human-readable
elif [[ "$file_type" =~ ^application/(vnd\.openxmlformats|msword|pdf) ]]; then
  echo "Article is a binary document (.xlsx/.docx/.pdf) - requires special parsing"
  # Would need xlsx2csv, docx2txt, or pdftotext tools
fi
```

2. **For extracted_content field**: If an article has `extracted_content`, it usually means the system extracted plain text from a binary attachment. This is your best option:
```bash
# Prefer extracted_content over resource.artifacts
extracted_url=$(jq -r '.article.extracted_content[0].original_url' article.json)
# This is usually plain text extraction from the binary file
```

3. **For Excel files in file paths**: Use conversion tools or note limitations:
```bash
# Cannot directly read binary files
if [[ "$file" == *.xlsx ]]; then
  echo "Note: Excel file requires conversion to CSV or JSON for processing"
  echo "Consider using: xlsx2csv, python openpyxl, or similar tools"
fi
```

**Prevention:**
- Always check `file.type` or `extracted_content` existence before downloading
- Add warnings when binary formats are detected
- Provide fallback instructions for manual extraction

---

## Issue #4 — Schema Location Discovery (@-reference confusion)

**Symptom:**
User references `@Use this/schemas` but initial file search returns empty

**Root Cause:**
- The `@` prefix is a user interface reference notation, not a filesystem path
- File search needs exact path: `Use this/schemas/`
- Spaces in path require proper escaping in shell commands

**Solution:**
1. **Always clarify path references**:
```
User says: "@Use this/schemas"
Actual path: "Use this/schemas/"
```

2. **Use Glob to discover files first**:
```bash
Glob(glob_pattern="Use this/**/*")
# Returns all files under "Use this/" directory
```

3. **Proper path escaping in shell**:
```bash
# Wrong
ls Use this/schemas/

# Correct
ls "Use this/schemas/"
```

**Prevention:**
- When user references `@path`, strip the `@` and verify with Glob
- Document that `@` is UI notation, not filesystem syntax
- Add validation step: "I found these files in `Use this/schemas/`: ..."

---

## Issue #5 — Large Article Content and Context Management

**Symptom:**
```
Article content is 32KB+ of text
Single article fetch returns 7500+ lines
Token usage spikes when reading multiple articles
```

**Root Cause:**
Knowledge base articles can be very large (BRD documents, detailed guides, etc.). Reading all content at once can exhaust context.

**Solution - Strategic Content Reading**:

1. **Metadata-first approach**:
```bash
# First, get just titles and IDs
curl -s -X POST 'https://api.devrev.ai/internal/articles.list' \
  -H "Authorization: ${ORG_PAT}" \
  -d '{}' | jq '.articles[] | {id, display_id, title}'
```

2. **Selective content fetching**:
```bash
# Only fetch articles that are clearly relevant
# For article list of 10 articles, user mentions "conversion logic"
# → Fetch only: ART-27 (BRD), ART-30 (Logic)
# → Skip: ART-52 (Login), ART-53 (Sitemap), etc.
```

3. **Partial reading with head/tail**:
```bash
# For very large articles, read first 500 lines to assess relevance
Read(path="/tmp/article.txt", limit=500)

# If relevant, read specific sections
Read(path="/tmp/article.txt", offset=1000, limit=300)
```

4. **Summarization before full read**:
```bash
# Extract key sections only
curl -s "$article_url" | grep -A 10 "## Section Title" > section.txt
```

**Prevention:**
- Ask user which specific articles/sections are most relevant
- Read article list first, let user prioritize
- Use `limit` parameter on Read tool for initial assessment
- Document typical article sizes in knowledge base index

---

## Issue #6 — Custom Object Schema Validation

**Symptom:**
Agent tries to use custom objects without verifying schema exists in org
Missing required fields in CreateXXX calls
Field type mismatches (string vs tokens, text vs rich_text)

**Root Cause:**
Custom object schemas vary by organization. Cannot assume schema structure without verification.

**Solution - Schema Discovery Before Use**:

1. **List available custom object types**:
```bash
curl -s -X POST 'https://api.devrev.ai/internal/schemas.custom.list' \
  -H "Authorization: ${ORG_PAT}" \
  -d '{}' | jq '.schemas[] | {leaf_type, description}'
```

2. **Fetch specific schema**:
```bash
curl -s -X POST 'https://api.devrev.ai/internal/schemas.custom.list' \
  -H "Authorization: ${ORG_PAT}" \
  -d '{"type": "raw_test_case"}' | jq '.schemas[0].fields[] | {name, field_type, description}'
```

3. **Validate required fields before Create**:
```bash
# Before calling CreateRawTestCase, verify:
# - All required fields are provided
# - Field types match schema (enum values, int ranges, etc.)
# - No extra fields that aren't in schema
```

4. **Add schema validation helper**:
```bash
validate_custom_object_payload() {
  local object_type="$1"
  local payload_file="$2"
  
  # Fetch schema
  local schema=$(curl -s -X POST 'https://api.devrev.ai/internal/schemas.custom.list' \
    -H "Authorization: ${ORG_PAT}" \
    -d "{\"type\": \"${object_type}\"}")
  
  # Extract required fields
  local required_fields=$(echo "$schema" | jq -r '.schemas[0].fields[] | select(.is_required == true) | .name')
  
  # Check payload has all required fields
  for field in $required_fields; do
    if ! jq -e ".${field}" "$payload_file" > /dev/null; then
      echo "Error: Missing required field: ${field}" >&2
      return 1
    fi
  done
  
  echo "Payload validation passed"
  return 0
}
```

**Prevention:**
- Always run schema discovery before first use of custom objects
- Cache schema definitions locally for session duration
- Add validation step in agent instructions: "Before using CreateXXX, verify schema with FetchObjectContext"

---

## Issue #7 — Skill Trigger Type Confusion

**Symptom:**
Agent configuration has skills with different trigger types:
- `trigger.operation` (native DevRev operations)
- `trigger.plan` (AI agent plans)
- `trigger.workflow` (snap-in workflows)

Unclear when to use each type.

**Root Cause:**
DevRev has three skill mechanisms with different purposes and invocation patterns.

**Solution - Skill Type Decision Tree**:

```
Does the skill need to:
├─ Query/modify DevRev objects (issues, articles, custom objects)?
│  └─ Use `trigger.operation` (native operations)
│     Examples: FetchObjectContext, HybridSearch, NLToSQL, 
│                CreateCustomObject, UpdateCustomObject
│
├─ Execute complex multi-step logic with its own agent?
│  └─ Use `trigger.plan` (AI agent plans)
│     Examples: ConvertTestCases (sub-agent), AnalyzeCode, 
│                GenerateReport (needs reasoning)
│
└─ Trigger external automation or business logic?
   └─ Use `trigger.workflow` (snap-in workflows)
      Examples: SendEmail, CreateJiraTicket, DeployToProduction,
                RunCICD, NotifySlack
```

**Documentation Requirement:**
Every skill in agent configuration should have:
```json
{
  "name": "SkillName",
  "description": "Clear description stating: (1) what it does, (2) when to use it, (3) what it returns",
  "trigger": {
    "operation": "don:integration:..."  // or plan, or workflow
  }
}
```

**Prevention:**
- Add skill type guide to SKILL.md
- Include decision tree in agent creation workflow
- Validate skill trigger types during agent improvement reviews

---

## Issue #8 — Agent Instruction Length and Clarity

**Symptom:**
Agent instructions become very long (500+ lines)
Hard to maintain consistency across sections
Unclear what takes precedence when rules conflict

**Root Cause:**
Complex agents require detailed instructions, but overly long prompts:
- Increase token usage
- Dilute critical information
- Risk internal inconsistencies

**Solution - Structured Instruction Template**:

```markdown
## Role & Persona
[2-3 sentences maximum, clear identity]

## Scope of Responsibilities
**You handle:**
- [Bullet list, 4-6 items max]

**You do NOT handle:**
- [Bullet list, clear boundaries]

## How to Respond
[Numbered workflow steps, 5-10 steps max]

### Special Case: [Scenario]
[Override rules for specific situations]

## When to Use Skills
[Table format: Skill | When to Use | Parameters]

## Escalation Rules
[3-5 clear escalation scenarios]

## Tone & Style
[3-5 communication guidelines]
```

**Key Principles:**
1. **Prioritize information**: Most critical rules first
2. **Use hierarchical structure**: Main rules → exceptions
3. **Avoid repetition**: State each rule once, reference it elsewhere
4. **Prefer tables over prose**: For skill usage, field mappings, etc.
5. **Link to external docs**: For detailed schemas, use "See schema_raw_test_case.json" instead of embedding full schema

**Prevention:**
- Set max instruction length target (300-400 lines)
- Regular review: Can this section be externalized or simplified?
- Test with subset of instructions first, add complexity only when needed

---

## Issue #9 — Testing Strategy Gaps

**Symptom:**
Agent works in development but fails in production with real data
Edge cases not covered
No systematic test coverage

**Root Cause:**
Testing is often ad-hoc or limited to happy path scenarios.

**Solution - Comprehensive Test Matrix**:

1. **Input Variation Testing**:
```
Test Category         | Scenarios
---------------------|------------------------------------------
Format variations    | Format 1 (10-col), Format 2 (9-col with continuation)
Volume               | Small (5 rows), Medium (50), Large (200+)
Data quality         | Clean, Missing fields, Malformed, Typos
Domain               | Instant Payment, Payment Activity, Mixed
```

2. **Pipeline Stage Testing**:
```bash
# Test each stage independently
Stage 1 (Ingest):     Can it parse both formats? Handle continuation rows?
Stage 2 (Normalize):  Correct domain classification? Pre-condition normalization?
Stage 3 (Convert):    Clustering logic? FIX rules applied? Column alignment?
Stage 4 (Validate):   M==R audit? All validation checks pass?
Stage 5 (Close):      Metrics correct? Batch status accurate?
```

3. **Error Scenario Testing**:
```
- Missing required fields
- Invalid enum values
- Duplicate raw IDs
- Empty files
- Network failures
- Permission errors
```

4. **Regression Test Suite**:
```bash
# Store known-good test cases
test_cases/
  ├── fiserv_format1_49rows.xlsx
  ├── fiserv_format2_continuation.xlsx
  ├── expected_output_format1.json
  └── test_runner.sh
```

**Prevention:**
- Create test suite before claiming "production-ready"
- Document test coverage in README
- Add CI/CD integration for automated testing
- Include test results in agent improvement reports

---

## Best Practices Summary

### Before Starting Agent Development
- [ ] Verify both `DEVREV_PAT` and `ORG_PAT` are configured
- [ ] Run `sync-knowledge.sh` to get latest guides
- [ ] Read `knowledge/INDEX.md` for overview
- [ ] Identify required custom object schemas (if any)
- [ ] List available skills and operations in org

### During Agent Creation
- [ ] Start with minimal instruction set (50-100 lines)
- [ ] Test with 1-2 examples before expanding
- [ ] Add skills one at a time, test each
- [ ] Document every skill's purpose and parameters
- [ ] Use tables/structured format for complex mappings

### Before Publishing Agent
- [ ] Run full test suite (happy path + edge cases)
- [ ] Verify M==R coverage for pipeline agents
- [ ] Check token usage (stay under 50% of limit if possible)
- [ ] Review all error messages for clarity
- [ ] Add troubleshooting section to agent description

### After Deployment
- [ ] Monitor first 10 real user interactions
- [ ] Collect feedback on failure modes
- [ ] Update instructions based on real-world edge cases
- [ ] Maintain changelog of prompt versions
- [ ] Regular review cycle (monthly for active agents)

---

## Quick Reference - Common Commands

### Check Network Permissions
```bash
# This will fail in sandbox:
curl -s https://api.devrev.ai/articles.list

# This works:
Shell(command="curl https://api.devrev.ai/articles.list", 
      required_permissions=["full_network"])
```

### Fetch Article with Fallback
```bash
# Get metadata first
article=$(curl -s -X POST 'https://api.devrev.ai/internal/articles.get' \
  -H "Authorization: ${ORG_PAT}" \
  -d '{"id": "don:core:dvrv-in-1:devo/X:article/Y"}')

# Try published version
body=$(echo "$article" | jq -r '.article.published_version.body // empty')

# Fallback to extracted content
if [ -z "$body" ]; then
  url=$(echo "$article" | jq -r '.article.extracted_content[0].original_url // empty')
  [ -n "$url" ] && curl -s "$url" > content.txt
fi
```

### Validate Custom Object Schema
```bash
# List all custom object types in org
curl -s -X POST 'https://api.devrev.ai/internal/schemas.custom.list' \
  -H "Authorization: ${ORG_PAT}" \
  -d '{}' | jq '.schemas[] | {leaf_type, id_prefix}'

# Get specific schema fields
curl -s -X POST 'https://api.devrev.ai/internal/schemas.custom.list' \
  -H "Authorization: ${ORG_PAT}" \
  -d '{"type": "raw_test_case"}' | \
  jq '.schemas[0].fields[] | {name, field_type, required: .is_required}'
```

### Test Agent with Bulk Inputs
```bash
# Create test input file
cat > test_inputs.json <<'EOF'
[
  {"input": "Create batch for file1.xlsx"},
  {"input": "Show batch status for BATCH-2026-06-02-120000"},
  {"input": "What's the M==R coverage?"}
]
EOF

# Run bulk test (requires test harness)
bash scripts/run-bulk-test.sh test_inputs.json
```

---

## Getting Help

1. **Check this troubleshooting guide first**
2. **Review `api-contracts.md`** for API-specific issues
3. **Read relevant knowledge base articles** in `knowledge/`
4. **Run diagnostic script**: `bash scripts/diagnose.sh`
5. **Check recent chat history** for similar issues
6. **Create detailed issue report** with:
   - Error message (full text)
   - Command/API call that failed
   - Expected vs actual behavior
   - Steps to reproduce

---

*Last Updated: 2026-06-02 based on real-world agent development sessions*
