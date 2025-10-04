# Contributing Guidelines – NASA Space Apps 2025

Welcome to our team repo! 🚀  
This is a hackathon project, so our focus is **speed, collaboration, and keeping `main` stable**.  

---

## 🔀 Branching Strategy

- **main** → always stable & demo-ready. Do **not** commit directly.  
- **integration** → used for daily merges and testing full pipeline.  
- **feature branches**:  
  - `backend-api` → Brice (backend, infra, CI/CD)  
  - `data-model` → Ainesh (data wrangling, EDA, ML model)  
  - optional: `ui-streamlit`, `docker-deploy` for stretch goals  

---

## 📦 Workflow

1. **Create branch from `main`:**

   ```bash
   git checkout main
   git pull origin main
   git checkout -b <branch-name>
   ```

2. **Push your branch:**

   ```bash
   git add .
   git commit -m "feat: add data preprocessing script"
   git push origin <branch-name>
   ```

3. **Open a Pull Request (PR) → `integration`:**
   - Title PR clearly (e.g., `feat: backend /predict endpoint`).
   - Keep PRs small and focused.  

4. **Daily merge into `integration`.**  
   - Once both sides work together (backend ↔ model), we merge into `main`.  

---

## ✅ Commit Message Convention

- `feat:` → new feature (`feat: add rain probability model`)  
- `fix:` → bug fix (`fix: API response schema`)  
- `chore:` → cleanup / CI / docs (`chore: add requirements.txt`)  
- `docs:` → documentation (`docs: add architecture.md draft`)  

---

## 🧪 Testing

- Run tests locally before pushing:  

   ```bash
   pytest
   ```

- CI will also run `ruff` (lint) and `pytest` on your branch.  

---

## 📖 Notes

- Keep `docs/` updated (plan, resources, architecture, pitch).  
- Use `notebooks/` for exploration only — final code should go in `src/`.  
- Communication: Discord + GitHub PR comments.  

---

💡 Remember: The goal is **a working MVP + clear presentation**, not perfection.  
