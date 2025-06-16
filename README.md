# 🧠 AI/ML Engineering with Python - Examples

This monorepo contains a collection of modular, end-to-end projects that demonstrate best practices for **AI/ML engineering** — from experimentation to production — with a focus on:

- MLOps & LLMOps patterns
- Real-world infrastructure integration
- CI/CD pipelines
- Evaluation, monitoring, and observability

These projects are designed to support a forthcoming book on **AI/ML Engineering**, and mirror the **full lifecycle of modern ML and LLM systems**.

---

## 📚 What This Repo Covers

Each project explores different slices of the AI/ML engineering stack, including:

- ✅ **Training & Experimentation**: with Ray, Kedro, classic ML, notebooks
- 🧠 **LLM Apps & Agents**: Bedrock, CrewAI, LangGraph, RAG workflows
- 🚀 **Deployment & Inference**: via Ray Serve, FastAPI, Bedrock, Lambda
- 📈 **Monitoring & Observability**: CloudWatch, Evidently AI, MLflow
- 🧪 **Evaluation**: model metrics, agent output quality, prompt tests
- 🔁 **CI/CD Workflows**: GitHub Actions, reusable runners, CT/CI patterns
- 🧰 **Infrastructure**: Terraform/CDK, Docker, Python envs

---

## 🏗️ Monorepo Structure

```text
projects/
├── ray-ml-pipeline/           # Ray Datasets, Train, Serve
├── kedro-ml-pipeline/         # Modular pipeline + optional MLflow
├── bedrock-rag-agent/         # Full-stack LLM app (client + server)
├── agent-frameworks/          # CrewAI, LangGraph, Pydantic-AI
├── classic-ml/                # Traditional models + CI
├── observability-pipelines/  # Lambda, CloudWatch, metrics
shared/                        # Common utilities across projects
evaluation/                    # Shared evaluation logic and runners
infra/                         # Optional shared Terraform/CDK modules
.github/                       # CI/CD workflows
