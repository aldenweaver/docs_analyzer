# Quick Test Guide - Verify UI Changes Work

## ⚠️ IMPORTANT: Why You're Not Seeing the Changes

The "View Analysis Results" and "View Fix Results" buttons **ONLY appear after a SUCCESSFUL analysis/fix completes**.

In your screenshot, I see an ERROR from a previous run:
```
Fix generation failed with return code 2
Error output:
usage: doc_fixer.py [-h] [--dry-run] [--no-backup] [--config CONFIG]
doc_fixer.py: error: unrecognized arguments: --format all
```

**This error is now fixed!** But you need to run a NEW analysis to see the buttons.

---

## ✅ Step-by-Step Test

### 1. Clear Any Old Errors
- **Reload the page** (Cmd+R or F5)
- If you still see the error box, it's from the old run
- The error is fixed in the backend now

### 2. Fill in the Form
```
Project Path: /Users/alden/dev/claude_docs_clone_mintlify
```
- Keep "Use Claude AI" unchecked for faster testing
- All analyzers selected is fine (or select just 1-2 for speed)
- Uncheck all fixers if you want fast test

### 3. Click "Run Analysis"

###4. Wait for Completion
- Progress bar will show "Running analysis with X analyzers..."
- Elapsed time will count up (e.g., "Elapsed: 5s", "Elapsed: 10s")
- When done, progress indicator disappears

### 5. Look for Buttons
**After success**, scroll down to the Results section. You should see:
- Summary cards (Total Issues, Files Analyzed, etc.)
- **"View Analysis Results"** button (if analysis succeeded)
- **"View Fix Results"** button (if fixers ran and succeeded)

### 6. Click "View Analysis Results"
- Should navigate to `/analysis-results`
- Should see summary cards at top
- Should see "Download Report" dropdown button
- Click dropdown to see: Download HTML, Download Markdown, Download JSON
- Should see HTML report displayed below

---

## 🐛 Common Issues

### "I don't see the buttons!"
**Checklist**:
1. ✅ Did the analysis complete successfully? (No error message?)
2. ✅ Do you see the Results section with summary cards?
3. ✅ Did the backend return `report_dir` in the response?

**How to check #3**:
- Open Browser DevTools (F12)
- Go to Network tab
- Look for `/api/analyze` request
- Click on it → Response tab
- Check if you see `"report_dir": "reports/YYYY-MM-DD_HH-MM-SS"`

If `report_dir` is missing, the buttons won't appear because there's no report to view!

### "The progress bar is stuck!"
- This was a bug - **now fixed** with `setElapsedTime(0)` in the finally block
- Try refreshing and running again

### "I get the --format error"
- This was fixed! The fixer no longer receives `--format all`
- Make sure the API server restarted (check terminal with the Python process)

---

## 🎯 Manual Verification Checklist

Run through this checklist to verify all changes:

- [ ] Progress indicator shows "Running analysis..." when started
- [ ] Elapsed timer counts up (updates every 100ms)
- [ ] Progress indicator disappears when done
- [ ] Elapsed timer resets to 0 after completion
- [ ] "Run Analysis" button is no longer disabled after completion
- [ ] Summary cards appear in Results section
- [ ] "View Analysis Results" button appears (if `report_dir` exists)
- [ ] "View Fix Results" button appears (if fixes ran and `report_dir` exists)
- [ ] Clicking "View Analysis Results" navigates to `/analysis-results`
- [ ] Analysis results page shows summary cards
- [ ] "Download Report" dropdown appears
- [ ] Dropdown has 3 options: HTML, Markdown, JSON
- [ ] Clicking an option downloads/opens the report
- [ ] HTML report displays inline on the page
- [ ] "Back to Analysis" button returns to main page

---

## 🔧 Technical Details

### Why Buttons Are Conditional

In `ui/app/page.tsx` lines 488-518:

```typescript
{analysisResult && analysisResult.report_dir && (
  <button onClick={() => { /* navigate to /analysis-results */ }}>
    View Analysis Results
  </button>
)}
```

**The button only renders if:**
1. `analysisResult` exists (analysis completed)
2. `analysisResult.report_dir` exists (backend returned report path)

### What the Backend Returns

After a successful analysis, the API returns:

```json
{
  "summary": {
    "total_issues": 42,
    "files_analyzed": 10
  },
  "issues": [...],
  "report_dir": "reports/2025-10-31_20-30-15",  ← THIS is required!
  "report_files": {
    "html": "doc_analysis_report.html",
    "markdown": "doc_analysis_report.md",
    "json": "doc_analysis_report.json"
  }
}
```

If `report_dir` is missing, the buttons won't appear.

---

## 🎬 Expected Behavior (Video Walkthrough)

1. **Initial State**: Form with empty project path
2. **After Form Fill**: Run Analysis button enabled
3. **During Analysis**:
   - Progress indicator visible
   - Timer counting: "Elapsed: 1s", "Elapsed: 2s", etc.
   - Button shows "Analyzing..."
4. **After Completion**:
   - Progress indicator gone
   - Timer reset to 0
   - Results section appears with cards
   - "View Analysis Results" button visible
5. **Click Button**:
   - URL changes to `/analysis-results`
   - New page loads with download dropdown
   - HTML report displays

---

## 📸 Screenshots to Take

To verify everything works, take these screenshots:

1. **Initial page** - Empty form
2. **Form filled** - Project path entered
3. **In progress** - Progress indicator with timer
4. **Completed** - Results section with View Results buttons
5. **Results page** - Analysis results with download dropdown
6. **Dropdown open** - Showing HTML/MD/JSON options

---

## 🚀 Quick Debug Commands

```bash
# Check if backend is running
curl http://localhost:8001/api/analyzers

# Check if frontend is running
curl http://localhost:3001

# Check API server logs
# (Look for the terminal running python3 main.py)

# Check if report files exist
ls -la /Users/alden/dev/docs_analyzer/reports/

# Check latest report directory
ls -lat /Users/alden/dev/docs_analyzer/reports/ | head -5
```

---

## ✅ All Changes Are Implemented

I've verified the code exists:
- ✅ `setElapsedTime(0)` on line 123 of page.tsx
- ✅ View Results buttons on lines 488-518
- ✅ Router import on line 4
- ✅ Results pages created
- ✅ Backend fixed (no --format for fixer)

**The changes ARE there - they just need a successful analysis to trigger!**

